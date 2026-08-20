from datetime import date
from unittest import IsolatedAsyncioTestCase
from uuid import UUID, uuid4

from app.agents.change_packet import ChangePacketNarrative, GroundedPacketInput
from app.domain.contracts import DependencyRecord, EvidenceKind, EvidenceRecord, RevisionRequest
from app.mcp.boundary import TraceStep
from app.services.demo_session import IdempotencyLedger
from app.services.revision_flow import ProductionMemory, RevisionFlow


class FakeMemory(ProductionMemory):
    def __init__(self) -> None:
        self.writes = 0

    async def append_revision(self, session_id: UUID, revision_id: UUID, idempotency_key: UUID, revision: RevisionRequest) -> TraceStep:
        self.writes += 1
        return TraceStep(step="writer_mcp", status="confirmed", public_detail="Revision event persisted.")

    async def read_evidence(self, scene_id: str):
        return [EvidenceRecord(evidence_id="ev-dailies-11-blue", scene_id="scene-11", kind=EvidenceKind.DAILIES, wardrobe_value="blue jacket", shoot_status="shot", excerpt="Blue jacket in scene 11.")]

    async def read_dependencies(self, scene_id: str):
        return [DependencyRecord(dependency_id="dep-12-13", source_scene_id="scene-12", target_scene_id="scene-13", shoot_date=date(2026, 8, 16), status="scheduled", evidence_id="ev-call-sheet-13")]


def request() -> RevisionRequest:
    return RevisionRequest(scene_id="scene-12", fact_type="wardrobe", old_value="blue jacket", new_value="black jacket")


class RevisionFlowTests(IsolatedAsyncioTestCase):
    async def test_happy_path_is_idempotent_and_grounded(self) -> None:
        memory = FakeMemory()

        async def agent(grounded: GroundedPacketInput) -> ChangePacketNarrative:
            return ChangePacketNarrative(status="ready", summary="Verified impact.", cited_evidence_ids=("ev-dailies-11-blue",), recommended_owners=("Wardrobe", "Assistant Director"), distinguishes_unknowns=True)

        flow = RevisionFlow(memory, agent, IdempotencyLedger())
        session_id, key = uuid4(), uuid4()
        first = await flow.apply(session_id, request(), key)
        second = await flow.apply(session_id, request(), key)
        self.assertEqual(first.revision_id, second.revision_id)
        self.assertEqual(memory.writes, 1)
        self.assertEqual(first.packet.status, "ready")

    async def test_invalid_agent_output_falls_back_without_losing_rules(self) -> None:
        memory = FakeMemory()

        async def agent(grounded: GroundedPacketInput) -> ChangePacketNarrative:
            return ChangePacketNarrative(status="ready", summary="Invented.", cited_evidence_ids=("not-real",), recommended_owners=("Wardrobe", "Assistant Director"), distinguishes_unknowns=True)

        result = await RevisionFlow(memory, agent, IdempotencyLedger()).apply(uuid4(), request(), uuid4())
        self.assertEqual(result.packet.status, "ready")
        self.assertEqual(result.trace[-1].status, "fallback")
        self.assertEqual(result.evaluation.findings[0].finding_type, "continuity_conflict")

    async def test_unconfigured_change_records_a_request_without_admitting_unrelated_evidence(self) -> None:
        memory = FakeMemory()

        async def agent(grounded: GroundedPacketInput) -> ChangePacketNarrative:
            return ChangePacketNarrative(status="review_required", summary="Human review required.", cited_evidence_ids=(), recommended_owners=(), distinguishes_unknowns=True)

        result = await RevisionFlow(memory, agent, IdempotencyLedger()).apply(
            uuid4(),
            RevisionRequest(scene_id="scene-12", fact_type="prop", old_value="sealed evidence bag", new_value="open evidence bag"),
            uuid4(),
        )
        self.assertEqual(memory.writes, 1)
        self.assertFalse(result.evaluation.can_create_followup)
        self.assertEqual(result.packet.cited_evidence_ids, ())
