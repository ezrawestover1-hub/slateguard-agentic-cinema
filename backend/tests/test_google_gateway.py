import json
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase

from app.agents.change_packet import GroundedPacketInput
from app.agents.gateway import AgentGatewayError, GoogleChangePacketGateway, create_change_packet_agent
from app.agents.runtime import GoogleAgentRuntimeTarget
from app.domain.contracts import ReadinessState


@dataclass
class Part:
    text: str


@dataclass
class Content:
    parts: list[Part]


@dataclass
class Event:
    content: Content
    final: bool

    def is_final_response(self) -> bool:
        return self.final


class Target:
    def __init__(self, events: list[Event]) -> None:
        self.events = events
        self.messages: list[str] = []

    async def async_stream_query(self, *, user_id: str, message: str):
        self.messages.append(message)
        for event in self.events:
            yield event


def grounded() -> GroundedPacketInput:
    return GroundedPacketInput(revision_id="r1", scene_id="scene-12", previous_value="blue jacket", new_value="black jacket", evidence_ids=("ev-1",), findings=(), readiness=ReadinessState.AT_RISK, can_create_followup=True)


class GoogleGatewayTests(IsolatedAsyncioTestCase):
    async def test_managed_target_resolves_once_and_streams_the_runtime_response(self) -> None:
        target = Target([Event(Content([Part("packet")]), True)])
        clients: list[object] = []

        class Engines:
            def __init__(self) -> None:
                self.requests: list[str] = []

            def get(self, *, name: str) -> Target:
                self.requests.append(name)
                return target

        engines = Engines()

        class Client:
            def __init__(self, **kwargs: str) -> None:
                self.kwargs = kwargs
                self.agent_engines = engines
                clients.append(self)

        runtime = GoogleAgentRuntimeTarget(
            project_id="project",
            location="us-central1",
            resource_name="projects/project/locations/us-central1/reasoningEngines/123",
            client_factory=Client,
        )
        first = [event async for event in runtime.async_stream_query(user_id="user", message="one")]
        second = [event async for event in runtime.async_stream_query(user_id="user", message="two")]
        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 1)
        self.assertEqual(engines.requests, ["projects/project/locations/us-central1/reasoningEngines/123"])
        self.assertIs(runtime._client, clients[0])

    async def test_gateway_uses_final_json_response_and_serializes_bounded_input(self) -> None:
        output = {"status": "ready", "summary": "Grounded.", "cited_evidence_ids": ["ev-1"], "recommended_owners": ["Wardrobe", "Assistant Director"], "distinguishes_unknowns": True}
        target = Target([Event(Content([Part("not final")]), False), Event(Content([Part(json.dumps(output))]), True)])
        result = await GoogleChangePacketGateway(target).generate(grounded())
        self.assertEqual(result.summary, "Grounded.")
        self.assertEqual(json.loads(target.messages[0])["evidence_ids"], ["ev-1"])

    async def test_gateway_fails_safely_without_a_final_response(self) -> None:
        with self.assertRaises(AgentGatewayError):
            await GoogleChangePacketGateway(Target([])).generate(grounded())

    async def test_gateway_accepts_mapping_shaped_runtime_events(self) -> None:
        output = {
            "status": "ready",
            "summary": "Grounded.",
            "cited_evidence_ids": ["ev-1"],
            "recommended_owners": ["Wardrobe", "Assistant Director"],
            "distinguishes_unknowns": True,
        }
        target = Target([])

        async def mapping_events(*, user_id: str, message: str):
            target.messages.append(message)
            yield {"content": {"parts": [{"text": "not final"}]}}
            yield {
                "finish_reason": "STOP",
                "content": {"parts": [{"text": json.dumps(output)}]},
            }

        target.async_stream_query = mapping_events  # type: ignore[method-assign]
        result = await GoogleChangePacketGateway(target).generate(grounded())
        self.assertEqual(result.summary, "Grounded.")

    async def test_agent_is_schema_constrained_to_change_packet_contract(self) -> None:
        agent = create_change_packet_agent()
        self.assertEqual(agent.name, "slateguard_change_packet")
        self.assertIsNotNone(agent.output_schema)
