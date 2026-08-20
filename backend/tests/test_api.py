from datetime import date
from unittest import TestCase
from unittest.mock import patch
from uuid import UUID

from fastapi.testclient import TestClient

from app.agents.change_packet import ChangePacketNarrative, GroundedPacketInput
from app.domain.contracts import DependencyRecord, EvidenceKind, EvidenceRecord, ImpactPulse
from app.main import ApplicationServices, create_app
from app.mcp.boundary import TraceStep
from app.services.demo_session import IdempotencyLedger, SessionSigner
from app.services.followup_flow import FollowupFlow, FollowupMemory
from app.services.revision_flow import ProductionMemory, RevisionFlow
from app.settings import Settings


class ApiMemory(ProductionMemory):
    async def append_revision(self, session_id: UUID, revision_id: UUID, idempotency_key: UUID) -> TraceStep:
        return TraceStep(step="writer_mcp", status="confirmed", public_detail="Revision event persisted.")

    async def read_evidence(self, scene_id: str):
        return [EvidenceRecord(evidence_id="ev-dailies-11-blue", scene_id="scene-11", kind=EvidenceKind.DAILIES, wardrobe_value="blue jacket", shoot_status="shot", excerpt="Blue jacket in scene 11.")]

    async def read_dependencies(self, scene_id: str):
        return [DependencyRecord(dependency_id="dep-12-13", source_scene_id="scene-12", target_scene_id="scene-13", shoot_date=date(2026, 8, 16), status="scheduled", evidence_id="ev-call-sheet-13")]


class ApiFollowupMemory(FollowupMemory):
    async def is_actionable(self, session_id: UUID, revision_id: UUID) -> bool:
        return True

    async def append_followup(self, session_id: UUID, action_id: UUID, revision_id: UUID) -> TraceStep:
        return TraceStep(step="writer_mcp", status="confirmed", public_detail="Follow-up action persisted.")

    async def append_readiness(self, session_id: UUID, revision_id: UUID) -> TraceStep:
        return TraceStep(step="writer_mcp", status="confirmed", public_detail="Readiness event persisted.")

    async def read_receipt_evidence(self, session_id: UUID, revision_id: UUID, action_id: UUID) -> tuple[str, ...]:
        return ("ev-dailies-11-blue", "ev-call-sheet-13", "ev-call-sheet-14")


class ApiImpactPulseMemory:
    async def read_impact_pulse(self) -> ImpactPulse:
        return ImpactPulse(
            scope="Scene 11 history · Scene 12 revision · next scheduled dependencies",
            relevant_evidence_records=4,
            active_scene_records=4,
            affected_scenes=2,
            scheduled_dependencies=2,
        )


async def api_agent(grounded: GroundedPacketInput) -> ChangePacketNarrative:
    return ChangePacketNarrative(status="ready", summary="Grounded packet.", cited_evidence_ids=("ev-dailies-11-blue",), recommended_owners=("Wardrobe", "Assistant Director"), distinguishes_unknowns=True)


class ApiTests(TestCase):
    def setUp(self) -> None:
        flow = RevisionFlow(ApiMemory(), api_agent, IdempotencyLedger())
        services = ApplicationServices(
            SessionSigner(b"test-secret", now=lambda: 1_000),
            flow,
            FollowupFlow(ApiFollowupMemory(), IdempotencyLedger()),
            ApiImpactPulseMemory(),
        )
        self.client = TestClient(create_app(Settings("test", __file__, True), services))

    def test_reset_mints_http_only_session_and_revision_runs_once(self) -> None:
        reset = self.client.post("/api/demo/reset")
        self.assertEqual(reset.status_code, 200)
        self.assertIn("HttpOnly", reset.headers["set-cookie"])
        payload = {"scene_id": "scene-12", "fact_type": "wardrobe", "old_value": "blue jacket", "new_value": "black jacket"}
        key = "00000000-0000-0000-0000-000000000099"
        first = self.client.post("/api/revisions", json=payload, headers={"Idempotency-Key": key})
        second = self.client.post("/api/revisions", json=payload, headers={"Idempotency-Key": key})
        self.assertEqual(first.status_code, 200)
        self.assertEqual(first.json()["revision_id"], second.json()["revision_id"])
        self.assertEqual(first.json()["packet"]["status"], "ready")

    def test_impact_pulse_exposes_only_curated_aggregate_counts(self) -> None:
        response = self.client.get("/api/impact-pulse")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["relevant_evidence_records"], 4)
        self.assertEqual(response.json()["scheduled_dependencies"], 2)
        self.assertNotIn("query", response.text)

    def test_reset_uses_services_built_at_runtime(self) -> None:
        flow = RevisionFlow(ApiMemory(), api_agent, IdempotencyLedger())
        runtime_services = ApplicationServices(
            SessionSigner(b"runtime-secret", now=lambda: 1_000),
            flow,
            FollowupFlow(ApiFollowupMemory(), IdempotencyLedger()),
        )
        with patch("app.bootstrap.build_services_from_environment", return_value=runtime_services):
            client = TestClient(create_app(Settings("test", __file__, True), None))
            reset = client.post("/api/demo/reset")

        self.assertEqual(reset.status_code, 200)
        self.assertIn("HttpOnly", reset.headers["set-cookie"])

    def test_followup_returns_reader_verified_receipt(self) -> None:
        self.client.post("/api/demo/reset")
        payload = {"scene_id": "scene-12", "fact_type": "wardrobe", "old_value": "blue jacket", "new_value": "black jacket"}
        revision = self.client.post("/api/revisions", json=payload, headers={"Idempotency-Key": "00000000-0000-0000-0000-000000000099"})
        receipt = self.client.post(
            f"/api/revisions/{revision.json()['revision_id']}/follow-up",
            json={"reviewed_evidence": True},
            headers={"Idempotency-Key": "00000000-0000-0000-0000-000000000100"},
        )
        self.assertEqual(receipt.status_code, 200)
        self.assertEqual(receipt.json()["readiness_to"], "Follow-up created")
        self.assertEqual(receipt.json()["trace"][-1]["step"], "reader_mcp")

    def test_followup_requires_explicit_evidence_acknowledgment(self) -> None:
        self.client.post("/api/demo/reset")
        payload = {"scene_id": "scene-12", "fact_type": "wardrobe", "old_value": "blue jacket", "new_value": "black jacket"}
        revision = self.client.post(
            "/api/revisions",
            json=payload,
            headers={"Idempotency-Key": "00000000-0000-0000-0000-000000000199"},
        )
        response = self.client.post(
            f"/api/revisions/{revision.json()['revision_id']}/follow-up",
            headers={"Idempotency-Key": "00000000-0000-0000-0000-000000000200"},
        )
        self.assertEqual(response.status_code, 422)

    def test_revision_fails_closed_without_session(self) -> None:
        client = TestClient(create_app(Settings("test", __file__, True), None))
        response = client.post("/api/revisions", json={"scene_id": "scene-12", "fact_type": "wardrobe", "old_value": "blue jacket", "new_value": "black jacket"}, headers={"Idempotency-Key": "00000000-0000-0000-0000-000000000099"})
        self.assertEqual(response.status_code, 503)
