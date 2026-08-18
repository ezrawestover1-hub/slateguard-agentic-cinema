from unittest import TestCase

from app.agents.change_packet import (
    ChangePacketNarrative,
    GroundedPacketInput,
    deterministic_fallback,
    validate_agent_packet,
)
from app.domain.contracts import FindingType, ReadinessState, RuleFinding


def actionable_input() -> GroundedPacketInput:
    return GroundedPacketInput(
        revision_id="revision-1",
        scene_id="scene-12",
        previous_value="blue jacket",
        new_value="black jacket",
        evidence_ids=("ev-dailies-11-blue", "ev-call-sheet-13", "ev-call-sheet-14"),
        findings=(
            RuleFinding(
                finding_type=FindingType.CONTINUITY_CONFLICT,
                evidence_ids=("ev-dailies-11-blue",),
                affected_scene_ids=("scene-11", "scene-12"),
            ),
        ),
        readiness=ReadinessState.AT_RISK,
        can_create_followup=True,
    )


class ChangePacketTests(TestCase):
    def test_grounded_packet_accepts_only_known_evidence_and_owners(self) -> None:
        grounded = actionable_input()
        candidate = ChangePacketNarrative(
            status="ready",
            summary="The new jacket conflicts with an already-shot continuity source.",
            cited_evidence_ids=("ev-dailies-11-blue",),
            recommended_owners=("Wardrobe", "Assistant Director"),
            distinguishes_unknowns=True,
        )
        self.assertIs(validate_agent_packet(candidate, grounded), candidate)

    def test_unknown_evidence_and_unapproved_owner_are_rejected(self) -> None:
        grounded = actionable_input()
        unknown = ChangePacketNarrative(
            status="ready", summary="Unsupported claim.", cited_evidence_ids=("invented-source",),
            recommended_owners=("Wardrobe", "Assistant Director"), distinguishes_unknowns=True,
        )
        with self.assertRaisesRegex(ValueError, "outside its grounded input"):
            validate_agent_packet(unknown, grounded)
        owner = ChangePacketNarrative(
            status="ready", summary="Unsupported owner.", cited_evidence_ids=("ev-dailies-11-blue",),
            recommended_owners=("Producer",), distinguishes_unknowns=True,
        )
        with self.assertRaisesRegex(ValueError, "unapproved"):
            validate_agent_packet(owner, grounded)

    def test_fallback_remains_factual_for_actionable_and_abstention_cases(self) -> None:
        ready = deterministic_fallback(actionable_input())
        self.assertEqual(ready.status, "ready")
        self.assertEqual(ready.recommended_owners, ("Wardrobe", "Assistant Director"))
        review_input = actionable_input().model_copy(update={"readiness": ReadinessState.REVIEW_REQUIRED, "can_create_followup": False})
        review = deterministic_fallback(review_input)
        self.assertEqual(review.status, "review_required")
        self.assertEqual(review.recommended_owners, ())
