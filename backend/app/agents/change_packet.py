"""Schema boundary for Gemini's explanatory, non-authoritative Change Packet role."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.domain.contracts import ReadinessState, RuleFinding


ALLOWED_OWNERS = ("Wardrobe", "Assistant Director")


class GroundedPacketInput(BaseModel):
    revision_id: str
    scene_id: str
    fact_type: str
    previous_value: str
    new_value: str
    evidence_ids: tuple[str, ...]
    findings: tuple[RuleFinding, ...]
    readiness: ReadinessState
    can_create_followup: bool


class ChangePacketNarrative(BaseModel):
    status: Literal["ready", "review_required"]
    summary: str = Field(min_length=1, max_length=500)
    cited_evidence_ids: tuple[str, ...]
    recommended_owners: tuple[str, ...] = ()
    distinguishes_unknowns: bool

    @model_validator(mode="after")
    def has_no_empty_citations(self) -> "ChangePacketNarrative":
        if self.status == "ready" and not self.cited_evidence_ids:
            raise ValueError("An actionable Change Packet must cite at least one source record.")
        return self


def validate_agent_packet(
    candidate: ChangePacketNarrative, grounded: GroundedPacketInput
) -> ChangePacketNarrative:
    """Accept only language that remains within deterministic evidence/authority bounds."""

    unknown_ids = set(candidate.cited_evidence_ids).difference(grounded.evidence_ids)
    if unknown_ids:
        raise ValueError("Agent cited evidence outside its grounded input.")
    if candidate.status == "ready" and not grounded.can_create_followup:
        raise ValueError("Agent cannot mark an abstention as ready.")
    if candidate.status == "review_required" and grounded.can_create_followup:
        raise ValueError("Agent cannot weaken an actionable deterministic result.")
    if candidate.recommended_owners and candidate.recommended_owners != ALLOWED_OWNERS:
        raise ValueError("Agent recommended an unapproved follow-up owner.")
    if candidate.status == "review_required" and candidate.recommended_owners:
        raise ValueError("Review-required packets cannot recommend a follow-up.")
    return candidate


def deterministic_fallback(grounded: GroundedPacketInput) -> ChangePacketNarrative:
    """Safe factual copy when the model is unavailable or returns invalid output."""

    if not grounded.can_create_followup:
        return ChangePacketNarrative(
            status="review_required",
            summary=(
                f"No configured evidence policy can safely automate this {grounded.fact_type} "
                f"change for {grounded.scene_id}. Human review is required."
            ),
            cited_evidence_ids=grounded.evidence_ids,
            recommended_owners=(),
            distinguishes_unknowns=True,
        )
    return ChangePacketNarrative(
        status="ready",
        summary="The revision conflicts with prior-shot footage and affects scheduled downstream scenes.",
        cited_evidence_ids=grounded.evidence_ids,
        recommended_owners=ALLOWED_OWNERS,
        distinguishes_unknowns=True,
    )
