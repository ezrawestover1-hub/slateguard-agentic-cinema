from datetime import date
from unittest import TestCase

from app.domain.contracts import DependencyRecord, EvidenceKind, EvidenceRecord, RevisionRequest
from app.services.rules import evaluate_revision


def revision() -> RevisionRequest:
    return RevisionRequest(
        scene_id="scene-12",
        fact_type="wardrobe",
        old_value="blue jacket",
        new_value="black jacket",
    )


def happy_evidence() -> list[EvidenceRecord]:
    return [
        EvidenceRecord(
            evidence_id="ev-dailies-11-blue",
            scene_id="scene-11",
            kind=EvidenceKind.DAILIES,
            wardrobe_value="blue jacket",
            shoot_status="shot",
            excerpt="Scene 11 dailies confirm Maya in blue jacket.",
        )
    ]


def happy_dependencies() -> list[DependencyRecord]:
    return [
        DependencyRecord(
            dependency_id="dep-12-13",
            source_scene_id="scene-12",
            target_scene_id="scene-13",
            shoot_date=date(2026, 8, 16),
            status="scheduled",
            evidence_id="ev-call-sheet-13",
        ),
        DependencyRecord(
            dependency_id="dep-12-14",
            source_scene_id="scene-12",
            target_scene_id="scene-14",
            shoot_date=date(2026, 8, 16),
            status="scheduled",
            evidence_id="ev-call-sheet-14",
        ),
    ]


class DeterministicRulesTests(TestCase):
    def test_happy_path_returns_exact_two_auditable_findings(self) -> None:
        result = evaluate_revision(revision(), happy_evidence(), happy_dependencies())
        self.assertTrue(result.can_create_followup)
        self.assertEqual(result.readiness, "At risk")
        self.assertEqual([finding.finding_type for finding in result.findings], ["continuity_conflict", "schedule_dependency"])
        self.assertEqual(result.findings[1].affected_scene_ids, ("scene-13", "scene-14"))

    def test_missing_dailies_abstains(self) -> None:
        result = evaluate_revision(revision(), [], happy_dependencies())
        self.assertFalse(result.can_create_followup)
        self.assertEqual(result.readiness, "Review required")
        self.assertEqual(result.findings, ())

    def test_contradictory_dailies_abstains_and_retains_both_sources(self) -> None:
        evidence = happy_evidence() + [
            EvidenceRecord(
                evidence_id="ev-dailies-11-black",
                scene_id="scene-11",
                kind=EvidenceKind.DAILIES,
                wardrobe_value="black jacket",
                shoot_status="shot",
                excerpt="Conflicting source record.",
            )
        ]
        result = evaluate_revision(revision(), evidence, happy_dependencies())
        self.assertFalse(result.can_create_followup)
        self.assertEqual(result.review_evidence_ids, ("ev-dailies-11-blue", "ev-dailies-11-black"))

    def test_unconfigured_change_is_recordable_but_requires_human_review(self) -> None:
        result = evaluate_revision(
            RevisionRequest(scene_id="scene-12", fact_type="prop", old_value="sealed evidence bag", new_value="open evidence bag"),
            happy_evidence(),
            happy_dependencies(),
        )
        self.assertFalse(result.can_create_followup)
        self.assertEqual(result.readiness, "Review required")
        self.assertIn("No evidence-backed automation policy", result.reason)

    def test_rejects_unsafe_change_text(self) -> None:
        with self.assertRaises(Exception):
            RevisionRequest(scene_id="scene-12", fact_type="prop", old_value="case'; DROP TABLE core.scenes", new_value="open case")
