import json
from pathlib import Path
from unittest import TestCase


class FixtureContractTests(TestCase):
    def test_evaluation_fixture_labels_are_unique_and_complete(self) -> None:
        fixture = Path(__file__).resolve().parents[2] / "clickhouse" / "fixtures" / "evaluations.json"
        cases = json.loads(fixture.read_text(encoding="utf-8"))["cases"]
        self.assertEqual(len({case["id"] for case in cases}), len(cases))
        self.assertEqual(cases[0]["expected_findings"], ["continuity_conflict", "schedule_dependency"])
        self.assertFalse(cases[1]["expected_followup"])
        self.assertFalse(cases[2]["expected_followup"])

    def test_seed_has_six_scenes_and_happy_path_source_ids(self) -> None:
        seed = (Path(__file__).resolve().parents[2] / "clickhouse" / "seed.sql").read_text(encoding="utf-8")
        for scene_id in ("scene-11", "scene-12", "scene-13", "scene-14", "scene-15", "scene-16"):
            self.assertIn(scene_id, seed)
        for evidence_id in ("ev-dailies-11-blue", "ev-call-sheet-13", "ev-call-sheet-14"):
            self.assertIn(evidence_id, seed)
