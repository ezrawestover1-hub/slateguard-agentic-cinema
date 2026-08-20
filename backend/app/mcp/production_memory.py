"""Typed production-memory adapter over the named ClickHouse MCP boundary."""

from __future__ import annotations

import asyncio
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from uuid import UUID

from app.domain.contracts import DependencyRecord, EvidenceRecord, ImpactPulse, RevisionRequest
from app.mcp.boundary import ClickHouseMcpBoundary, McpBoundaryError, TraceStep
from app.services.followup_flow import FollowupMemory
from app.services.revision_flow import ProductionMemory


@dataclass(slots=True)
class ClickHouseProductionMemory(ProductionMemory):
    """Translate fixed curated-result shapes into application contracts."""

    boundary: ClickHouseMcpBoundary

    async def append_revision(
        self, session_id: UUID, revision_id: UUID, idempotency_key: UUID, revision: RevisionRequest
    ) -> TraceStep:
        return await self.boundary.write_revision_event(session_id, revision_id, idempotency_key, revision)

    async def read_evidence(self, scene_id: str) -> Sequence[EvidenceRecord]:
        raw_result, _ = await self.boundary.read_scene_evidence(scene_id)
        return tuple(EvidenceRecord.model_validate(row) for row in _rows(raw_result))

    async def read_dependencies(self, scene_id: str) -> Sequence[DependencyRecord]:
        raw_result, _ = await self.boundary.read_scheduled_dependencies(scene_id)
        records = []
        for row in _rows(raw_result):
            normalized = dict(row)
            normalized["shoot_date"] = date.fromisoformat(str(normalized["shoot_date"]))
            records.append(DependencyRecord.model_validate(normalized))
        return tuple(records)

    async def read_impact_pulse(self) -> ImpactPulse:
        """Return an auditable aggregate over the active production window only."""

        (evidence_result, _), (dependency_result, _) = await asyncio.gather(
            self.boundary.read_relevance_evidence(),
            self.boundary.read_relevance_dependencies(),
        )
        evidence_rows = _rows(evidence_result)
        dependency_rows = _rows(dependency_result)
        if len(evidence_rows) != 1 or len(dependency_rows) != 1:
            raise McpBoundaryError("ClickHouse returned an unexpected impact pulse.")

        return ImpactPulse(
            scope="Scene 11 history · Scene 12 revision · next scheduled dependencies",
            relevant_evidence_records=_required_count(evidence_rows[0], "relevant_evidence_records"),
            active_scene_records=_required_count(evidence_rows[0], "active_scene_records"),
            affected_scenes=_required_count(dependency_rows[0], "affected_scenes"),
            scheduled_dependencies=_required_count(dependency_rows[0], "scheduled_dependencies"),
        )


@dataclass(slots=True)
class ClickHouseFollowupMemory(FollowupMemory):
    """Persist a human decision and verify its receipt through curated reads."""

    boundary: ClickHouseMcpBoundary

    async def is_actionable(self, session_id: UUID, revision_id: UUID) -> bool:
        raw_result, _ = await self.boundary.read_actionable_revision(session_id, revision_id)
        return bool(_rows(raw_result))

    async def append_followup(
        self, session_id: UUID, action_id: UUID, revision_id: UUID
    ) -> TraceStep:
        return await self.boundary.write_followup_event(session_id, action_id, revision_id)

    async def append_readiness(self, session_id: UUID, revision_id: UUID) -> TraceStep:
        return await self.boundary.write_readiness_event(session_id, revision_id)

    async def read_receipt_evidence(
        self, session_id: UUID, revision_id: UUID, action_id: UUID
    ) -> tuple[str, ...]:
        (receipt, _), (evidence, _), (dependencies, _) = await asyncio.gather(
            self.boundary.read_followup_receipt(session_id, revision_id, action_id),
            self.boundary.read_scene_evidence("scene-12"),
            self.boundary.read_scheduled_dependencies("scene-12"),
        )
        if not _rows(receipt):
            raise McpBoundaryError("ClickHouse did not confirm the follow-up receipt.")
        evidence_ids = [
            str(row["evidence_id"])
            for row in _rows(evidence)
            if row.get("kind") == "dailies"
        ]
        evidence_ids.extend(str(row["evidence_id"]) for row in _rows(dependencies))
        return tuple(dict.fromkeys(evidence_ids))


def _rows(raw_result: str) -> tuple[Mapping[str, object], ...]:
    """Decode the official server's ``columns``/``rows`` JSON without raw SQL."""

    try:
        decoded = json.loads(raw_result)
        columns = decoded["columns"]
        rows = decoded["rows"]
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise McpBoundaryError("ClickHouse returned an unexpected curated result.") from error
    if not isinstance(columns, list) or not isinstance(rows, list):
        raise McpBoundaryError("ClickHouse returned an unexpected curated result.")

    records: list[Mapping[str, object]] = []
    for row in rows:
        if not isinstance(row, list) or len(row) != len(columns) or not all(
            isinstance(column, str) for column in columns
        ):
            raise McpBoundaryError("ClickHouse returned an unexpected curated result.")
        records.append(dict(zip(columns, row, strict=True)))
    return tuple(records)


def _required_count(row: Mapping[str, object], field: str) -> int:
    value = row.get(field)
    if isinstance(value, bool):
        raise McpBoundaryError("ClickHouse returned an unexpected impact pulse.")
    try:
        count = int(value)
    except (TypeError, ValueError) as error:
        raise McpBoundaryError("ClickHouse returned an unexpected impact pulse.") from error
    if count < 0:
        raise McpBoundaryError("ClickHouse returned an unexpected impact pulse.")
    return count
