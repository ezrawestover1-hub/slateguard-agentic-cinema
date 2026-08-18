import json
from datetime import date
from unittest import IsolatedAsyncioTestCase

from app.mcp.boundary import ClickHouseMcpBoundary
from app.mcp.production_memory import ClickHouseFollowupMemory, ClickHouseProductionMemory


class ProductionMemoryTests(IsolatedAsyncioTestCase):
    async def test_curated_rows_are_mapped_to_typed_evidence_and_dependencies(self) -> None:
        async def runner(identity: str, query: str) -> str:
            if "mart.sg_scene_evidence" in query:
                return json.dumps(
                    {
                        "columns": [
                            "evidence_id", "scene_id", "kind", "wardrobe_value", "shoot_status", "excerpt"
                        ],
                        "rows": [["ev-dailies-11-blue", "scene-11", "dailies", "blue jacket", "shot", "Scene 11 dailies."]],
                    }
                )
            return json.dumps(
                {
                    "columns": ["dependency_id", "source_scene_id", "target_scene_id", "shoot_date", "status", "evidence_id"],
                    "rows": [["dep-12-13", "scene-12", "scene-13", "2026-08-16", "scheduled", "ev-call-sheet-13"]],
                }
            )

        memory = ClickHouseProductionMemory(ClickHouseMcpBoundary(runner))
        evidence = await memory.read_evidence("scene-12")
        dependencies = await memory.read_dependencies("scene-12")
        self.assertEqual(evidence[0].evidence_id, "ev-dailies-11-blue")
        self.assertEqual(dependencies[0].shoot_date, date(2026, 8, 16))

    async def test_followup_receipt_uses_reader_confirmed_action_and_evidence(self) -> None:
        async def runner(identity: str, query: str) -> str:
            if "sg_actionable_revisions" in query or "sg_followup_receipts" in query:
                return json.dumps({"columns": ["revision_id"], "rows": [["r1"]]})
            if "sg_scene_evidence" in query:
                return json.dumps(
                    {
                        "columns": ["evidence_id", "kind"],
                        "rows": [["ev-dailies-11-blue", "dailies"], ["ev-fact-12-blue", "fact"]],
                    }
                )
            return json.dumps(
                {
                    "columns": ["evidence_id"],
                    "rows": [["ev-call-sheet-13"], ["ev-call-sheet-14"]],
                }
            )

        memory = ClickHouseFollowupMemory(ClickHouseMcpBoundary(runner))
        from uuid import uuid4

        session_id, revision_id, action_id = uuid4(), uuid4(), uuid4()
        self.assertTrue(await memory.is_actionable(session_id, revision_id))
        receipt_evidence = await memory.read_receipt_evidence(session_id, revision_id, action_id)
        self.assertEqual(receipt_evidence, ("ev-dailies-11-blue", "ev-call-sheet-13", "ev-call-sheet-14"))

    async def test_impact_pulse_is_derived_from_two_curated_aggregate_results(self) -> None:
        async def runner(identity: str, query: str) -> str:
            if "relevant_evidence_records" in query:
                return json.dumps(
                    {
                        "columns": ["relevant_evidence_records", "active_scene_records"],
                        "rows": [[4, 4]],
                    }
                )
            return json.dumps(
                {
                    "columns": ["affected_scenes", "scheduled_dependencies"],
                    "rows": [[2, 2]],
                }
            )

        pulse = await ClickHouseProductionMemory(ClickHouseMcpBoundary(runner)).read_impact_pulse()
        self.assertEqual(pulse.relevant_evidence_records, 4)
        self.assertEqual(pulse.affected_scenes, 2)
        self.assertIn("Scene 12 revision", pulse.scope)
