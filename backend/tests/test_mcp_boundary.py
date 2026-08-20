from unittest import IsolatedAsyncioTestCase
from uuid import uuid4

from app.mcp.boundary import ClickHouseMcpBoundary, McpBoundaryError
from app.domain.contracts import RevisionRequest


class McpBoundaryTests(IsolatedAsyncioTestCase):
    async def test_reader_path_uses_curated_view_and_never_accepts_sql(self) -> None:
        calls: list[tuple[str, str]] = []

        async def runner(identity: str, query: str) -> str:
            calls.append((identity, query))
            return "[]"

        result, trace = await ClickHouseMcpBoundary(runner).read_scene_evidence("scene-12")
        self.assertEqual(result, "[]")
        self.assertEqual(trace.status, "confirmed")
        self.assertEqual(calls[0][0], "reader")
        self.assertIn("FROM mart.sg_scene_evidence", calls[0][1])
        self.assertIn("'scene-11'", calls[0][1])
        self.assertNotIn("INSERT", calls[0][1])

    async def test_writer_path_only_uses_prepared_revision_values(self) -> None:
        calls: list[tuple[str, str]] = []

        async def runner(identity: str, query: str) -> str:
            calls.append((identity, query))
            return "ok"

        trace = await ClickHouseMcpBoundary(runner).write_revision_event(
            uuid4(),
            uuid4(),
            uuid4(),
            RevisionRequest(scene_id="scene-12", fact_type="wardrobe", old_value="blue jacket", new_value="black jacket"),
        )
        self.assertEqual(trace.public_detail, "Revision event persisted.")
        self.assertEqual(calls[0][0], "writer")
        self.assertIn("'scene-12', 'wardrobe', 'blue jacket', 'black jacket'", calls[0][1])
        self.assertNotIn("SELECT", calls[0][1])

    async def test_relevance_aggregates_are_fixed_to_curated_active_scope(self) -> None:
        calls: list[tuple[str, str]] = []

        async def runner(identity: str, query: str) -> str:
            calls.append((identity, query))
            return '{"columns": [], "rows": []}'

        boundary = ClickHouseMcpBoundary(runner)
        await boundary.read_relevance_evidence()
        await boundary.read_relevance_dependencies()
        self.assertEqual([identity for identity, _ in calls], ["reader", "reader"])
        self.assertIn("mart.sg_scene_evidence", calls[0][1])
        self.assertIn("'scene-11'", calls[0][1])
        self.assertIn("mart.sg_scheduled_dependencies", calls[1][1])
        self.assertIn("source_scene_id = 'scene-12'", calls[1][1])
        self.assertNotIn("core.", calls[0][1] + calls[1][1])

    async def test_unknown_scene_is_rejected_before_mcp_invocation(self) -> None:
        async def runner(identity: str, query: str) -> str:
            raise AssertionError("runner must not be called")

        with self.assertRaises(ValueError):
            await ClickHouseMcpBoundary(runner).read_scene_evidence("scene-12'; DROP TABLE core.scenes")

    async def test_followup_queries_are_session_scoped_and_reader_verified(self) -> None:
        calls: list[tuple[str, str]] = []

        async def runner(identity: str, query: str) -> str:
            calls.append((identity, query))
            return '{"columns": [], "rows": []}'

        boundary = ClickHouseMcpBoundary(runner)
        session_id, revision_id, action_id = uuid4(), uuid4(), uuid4()
        await boundary.read_actionable_revision(session_id, revision_id)
        await boundary.write_followup_event(session_id, action_id, revision_id)
        await boundary.write_readiness_event(session_id, revision_id)
        await boundary.read_followup_receipt(session_id, revision_id, action_id)
        self.assertEqual([call[0] for call in calls], ["reader", "writer", "writer", "reader"])
        self.assertIn("mart.sg_followup_receipts", calls[-1][1])
        self.assertIn(str(session_id), calls[-1][1])

    async def test_internal_error_is_redacted_for_public_callers(self) -> None:
        async def runner(identity: str, query: str) -> str:
            raise RuntimeError("password=not-for-public-output")

        with self.assertRaisesRegex(McpBoundaryError, "evidence path is unavailable"):
            await ClickHouseMcpBoundary(runner).read_scene_evidence("scene-12")
