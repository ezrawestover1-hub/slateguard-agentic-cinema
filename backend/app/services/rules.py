"""Deterministic rules: facts in, auditable findings out, no model dependency."""

from __future__ import annotations

from collections.abc import Sequence

from app.domain.contracts import (
    DependencyRecord,
    EvidenceKind,
    EvidenceRecord,
    FindingType,
    ReadinessState,
    RevisionRequest,
    RuleEvaluation,
    RuleFinding,
)


def evaluate_revision(
    revision: RevisionRequest,
    evidence: Sequence[EvidenceRecord],
    dependencies: Sequence[DependencyRecord],
) -> RuleEvaluation:
    """Evaluate an intake request against the available curated policy.

    Missing or inconsistent evidence abstains before any follow-up is possible.
    The caller is responsible for retrieving these records through the reader MCP
    adapter; this pure function never performs I/O or composes SQL.
    """

    if not _has_actionable_policy(revision):
        return _review_required(
            (),
            f"No evidence-backed automation policy is configured for this {revision.fact_type} change in {revision.scene_id}.",
        )

    prior_dailies = [
        record
        for record in evidence
        if record.kind == EvidenceKind.DAILIES and record.scene_id == "scene-11"
    ]
    if not prior_dailies:
        return _review_required((), "No prior-shot dailies evidence is available.")

    values = {record.wardrobe_value for record in prior_dailies if record.wardrobe_value}
    evidence_ids = tuple(record.evidence_id for record in prior_dailies)
    if not values or len(values) != 1:
        return _review_required(evidence_ids, "Prior-shot dailies disagree about wardrobe continuity.")
    if revision.old_value not in values:
        return _review_required(evidence_ids, "Prior-shot dailies do not confirm the revised baseline.")

    scheduled = [
        dependency
        for dependency in dependencies
        if dependency.source_scene_id == revision.scene_id and dependency.status == "scheduled"
    ]
    if not scheduled:
        return _review_required(evidence_ids, "No scheduled downstream dependency evidence is available.")

    schedule_evidence_ids = tuple(dependency.evidence_id for dependency in scheduled)
    scheduled_scene_ids = tuple(dependency.target_scene_id for dependency in scheduled)
    findings = (
        RuleFinding(
            finding_type=FindingType.CONTINUITY_CONFLICT,
            evidence_ids=evidence_ids,
            affected_scene_ids=("scene-11", revision.scene_id),
        ),
        RuleFinding(
            finding_type=FindingType.SCHEDULE_DEPENDENCY,
            evidence_ids=schedule_evidence_ids,
            affected_scene_ids=scheduled_scene_ids,
        ),
    )
    return RuleEvaluation(
        readiness=ReadinessState.AT_RISK,
        findings=findings,
        can_create_followup=True,
        reason="Prior-shot continuity and scheduled downstream work require review.",
    )


def _has_actionable_policy(revision: RevisionRequest) -> bool:
    """Keep the public demo honest: only a proven rule can make an action available."""

    return (
        revision.scene_id == "scene-12"
        and revision.fact_type == "wardrobe"
        and revision.old_value.casefold() == "blue jacket"
    )


def _review_required(evidence_ids: tuple[str, ...], reason: str) -> RuleEvaluation:
    return RuleEvaluation(
        readiness=ReadinessState.REVIEW_REQUIRED,
        review_evidence_ids=evidence_ids,
        can_create_followup=False,
        reason=reason,
    )
