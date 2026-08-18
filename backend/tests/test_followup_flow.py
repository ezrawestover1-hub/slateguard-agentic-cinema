from unittest import IsolatedAsyncioTestCase
from uuid import UUID, uuid4

from app.mcp.boundary import TraceStep
from app.services.demo_session import IdempotencyLedger
from app.services.followup_flow import FollowupFlow, FollowupMemory, FollowupNotAllowed


class FakeFollowupMemory(FollowupMemory):
    def __init__(self, actionable: bool = True) -> None:
        self.actionable = actionable
        self.writes = 0

    async def is_actionable(self, session_id: UUID, revision_id: UUID) -> bool:
        return self.actionable

    async def append_followup(self, session_id: UUID, action_id: UUID, revision_id: UUID) -> TraceStep:
        self.writes += 1
        return TraceStep(step="writer_mcp", status="confirmed", public_detail="Follow-up action persisted.")

    async def append_readiness(self, session_id: UUID, revision_id: UUID) -> TraceStep:
        self.writes += 1
        return TraceStep(step="writer_mcp", status="confirmed", public_detail="Readiness event persisted.")

    async def read_receipt_evidence(self, session_id: UUID, revision_id: UUID, action_id: UUID) -> tuple[str, ...]:
        return ("ev-dailies-11-blue", "ev-call-sheet-13", "ev-call-sheet-14")


class FollowupFlowTests(IsolatedAsyncioTestCase):
    async def test_action_is_human_owned_reader_verified_and_idempotent(self) -> None:
        memory = FakeFollowupMemory()
        flow = FollowupFlow(memory, IdempotencyLedger())
        session, revision, key = uuid4(), uuid4(), uuid4()
        first = await flow.create(session, revision, key)
        second = await flow.create(session, revision, key)
        self.assertEqual(first.action_id, second.action_id)
        self.assertEqual(memory.writes, 2)
        self.assertEqual(first.owners, ("Wardrobe", "Assistant Director"))
        self.assertEqual(first.readiness_to, "Follow-up created")
        self.assertEqual(first.trace[-1].step, "reader_mcp")

    async def test_non_actionable_revision_never_creates_followup(self) -> None:
        memory = FakeFollowupMemory(actionable=False)
        with self.assertRaises(FollowupNotAllowed):
            await FollowupFlow(memory, IdempotencyLedger()).create(uuid4(), uuid4(), uuid4())
        self.assertEqual(memory.writes, 0)
