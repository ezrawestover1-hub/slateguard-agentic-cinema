"""Contracts shared by the future MCP adapters, rules, agent, and API routes."""

from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class EvidenceKind(StrEnum):
    DAILIES = "dailies"
    FACT = "fact"
    CALL_SHEET = "call_sheet"


class RevisionRequest(BaseModel):
    """A bounded production-change request accepted from the command desk.

    These fields remain deliberately constrained because the values are persisted
    by a server-owned ClickHouse template. A request can be recorded even when
    there is not yet an evidence-backed automation policy for it.
    """

    scene_id: str = Field(pattern=r"^scene-(?:1[1-6])$")
    fact_type: Literal["wardrobe", "prop", "set dressing", "blocking", "schedule"]
    old_value: str = Field(min_length=1, max_length=120)
    new_value: str = Field(min_length=1, max_length=120)

    @field_validator("old_value", "new_value")
    @classmethod
    def normalizes_safe_text(cls, value: str) -> str:
        normalized = " ".join(value.split())
        allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,'’&()/+-")
        if not normalized or any(character not in allowed for character in normalized):
            raise ValueError("Change values may contain letters, numbers, and standard production-note punctuation.")
        return normalized

    @model_validator(mode="after")
    def describes_a_real_change(self) -> "RevisionRequest":
        if self.old_value.casefold() == self.new_value.casefold():
            raise ValueError("The proposed value must differ from the current value.")
        return self


class FollowupRequest(BaseModel):
    """Explicit human acknowledgement required before a durable follow-up."""

    reviewed_evidence: Literal[True]


class EvidenceRecord(BaseModel):
    evidence_id: str
    scene_id: str
    kind: EvidenceKind
    wardrobe_value: str | None = None
    shoot_status: str | None = None
    excerpt: str


class DependencyRecord(BaseModel):
    dependency_id: str
    source_scene_id: str
    target_scene_id: str
    shoot_date: date
    status: str
    evidence_id: str


class ImpactPulse(BaseModel):
    """A bounded, reader-derived summary of the active production window."""

    scope: str
    relevant_evidence_records: int = Field(ge=0)
    active_scene_records: int = Field(ge=0)
    affected_scenes: int = Field(ge=0)
    scheduled_dependencies: int = Field(ge=0)


class FindingType(StrEnum):
    CONTINUITY_CONFLICT = "continuity_conflict"
    SCHEDULE_DEPENDENCY = "schedule_dependency"


class ReadinessState(StrEnum):
    AT_RISK = "At risk"
    REVIEW_REQUIRED = "Review required"


class RuleFinding(BaseModel):
    finding_type: FindingType
    evidence_ids: tuple[str, ...]
    affected_scene_ids: tuple[str, ...]


class RuleEvaluation(BaseModel):
    readiness: ReadinessState
    findings: tuple[RuleFinding, ...] = ()
    review_evidence_ids: tuple[str, ...] = ()
    can_create_followup: bool
    reason: str = Field(min_length=1)
