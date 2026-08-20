"""Named ClickHouse templates and safe, public trace results."""

from __future__ import annotations

import re
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel

from app.domain.contracts import RevisionRequest


class ReaderTemplate(StrEnum):
    SCENE_EVIDENCE = "scene_evidence"
    SCHEDULED_DEPENDENCIES = "scheduled_dependencies"
    RELEVANCE_EVIDENCE = "relevance_evidence"
    RELEVANCE_DEPENDENCIES = "relevance_dependencies"
    ACTIONABLE_REVISION = "actionable_revision"
    FOLLOWUP_RECEIPT = "followup_receipt"


class WriterTemplate(StrEnum):
    REVISION_EVENT = "revision_event"
    FOLLOWUP_EVENT = "followup_event"
    READINESS_EVENT = "readiness_event"


class McpBoundaryError(RuntimeError):
    """Deliberately non-diagnostic error safe for the public API."""


class TraceStep(BaseModel):
    step: str
    status: str
    public_detail: str


QueryRunner = Callable[[str, str], Awaitable[str]]
_SCENE_ID = re.compile(r"^scene-(?:1[1-6])$")


@dataclass(frozen=True, slots=True)
class ClickHouseMcpBoundary:
    """Only server-owned templates may cross the official MCP process boundary."""

    run_query: QueryRunner

    async def read_scene_evidence(self, scene_id: str) -> tuple[str, TraceStep]:
        _require_scene_id(scene_id)
        return await self._execute(
            "reader",
            ReaderTemplate.SCENE_EVIDENCE,
            "SELECT evidence_id, scene_id, kind, wardrobe_value, shoot_status, excerpt "
            "FROM mart.sg_scene_evidence "
            "WHERE scene_id IN ('scene-11', 'scene-12', 'scene-13', 'scene-14') "
            "ORDER BY occurred_at ASC",
            "Evidence retrieved through the reader MCP path.",
        )

    async def read_scheduled_dependencies(self, scene_id: str) -> tuple[str, TraceStep]:
        _require_scene_id(scene_id)
        return await self._execute(
            "reader",
            ReaderTemplate.SCHEDULED_DEPENDENCIES,
            "SELECT dependency_id, source_scene_id, target_scene_id, shoot_date, status, evidence_id "
            "FROM mart.sg_scheduled_dependencies "
            f"WHERE source_scene_id = '{scene_id}' ORDER BY target_scene_id ASC",
            "Scheduled dependencies retrieved through the reader MCP path.",
        )

    async def read_relevance_evidence(self) -> tuple[str, TraceStep]:
        """Aggregate only the evidence records relevant to the prepared revision."""

        return await self._execute(
            "reader",
            ReaderTemplate.RELEVANCE_EVIDENCE,
            "SELECT countDistinct(evidence_id) AS relevant_evidence_records, "
            "countDistinct(scene_id) AS active_scene_records "
            "FROM mart.sg_scene_evidence "
            "WHERE scene_id IN ('scene-11', 'scene-12', 'scene-13', 'scene-14')",
            "Active evidence scope aggregated through the reader MCP path.",
        )

    async def read_relevance_dependencies(self) -> tuple[str, TraceStep]:
        """Aggregate only scheduled work affected by the prepared revision."""

        return await self._execute(
            "reader",
            ReaderTemplate.RELEVANCE_DEPENDENCIES,
            "SELECT countDistinct(target_scene_id) AS affected_scenes, "
            "count() AS scheduled_dependencies "
            "FROM mart.sg_scheduled_dependencies "
            "WHERE source_scene_id = 'scene-12'",
            "Scheduled impact scope aggregated through the reader MCP path.",
        )

    async def write_revision_event(
        self, demo_session_id: UUID, revision_id: UUID, idempotency_key: UUID, revision: RevisionRequest
    ) -> TraceStep:
        _require_scene_id(revision.scene_id)
        await self._execute(
            "writer",
            WriterTemplate.REVISION_EVENT,
            "INSERT INTO core.revision_events "
            "(demo_session_id, revision_id, scene_id, fact_type, old_value, new_value, idempotency_key, recorded_at) "
            "VALUES "
            f"('{demo_session_id}', '{revision_id}', {_quote(revision.scene_id)}, {_quote(revision.fact_type)}, "
            f"{_quote(revision.old_value)}, {_quote(revision.new_value)}, '{idempotency_key}', now64(3))",
            "Revision recorded through the writer MCP path.",
        )
        return TraceStep(step="writer_mcp", status="confirmed", public_detail="Revision event persisted.")

    async def read_actionable_revision(self, demo_session_id: UUID, revision_id: UUID) -> tuple[str, TraceStep]:
        return await self._execute(
            "reader",
            ReaderTemplate.ACTIONABLE_REVISION,
            "SELECT revision_id FROM mart.sg_actionable_revisions "
            f"WHERE demo_session_id = toUUID('{demo_session_id}') "
            f"AND revision_id = toUUID('{revision_id}') LIMIT 1",
            "Revision actionability retrieved through the reader MCP path.",
        )

    async def write_followup_event(
        self, demo_session_id: UUID, action_id: UUID, revision_id: UUID
    ) -> TraceStep:
        await self._execute(
            "writer",
            WriterTemplate.FOLLOWUP_EVENT,
            "INSERT INTO core.followup_action_events "
            "(demo_session_id, action_id, revision_id, owners, status, created_at) VALUES "
            f"('{demo_session_id}', '{action_id}', '{revision_id}', "
            "['Wardrobe', 'Assistant Director'], 'Follow-up created', now64(3))",
            "Follow-up action recorded through the writer MCP path.",
        )
        return TraceStep(step="writer_mcp", status="confirmed", public_detail="Follow-up action persisted.")

    async def write_readiness_event(self, demo_session_id: UUID, revision_id: UUID) -> TraceStep:
        readiness_event_id = uuid4()
        await self._execute(
            "writer",
            WriterTemplate.READINESS_EVENT,
            "INSERT INTO core.readiness_events "
            "(demo_session_id, readiness_event_id, revision_id, state, reason, recorded_at) VALUES "
            f"('{demo_session_id}', '{readiness_event_id}', '{revision_id}', "
            "'Follow-up created', 'Wardrobe and Assistant Director follow-up created.', now64(3))",
            "Readiness transition recorded through the writer MCP path.",
        )
        return TraceStep(step="writer_mcp", status="confirmed", public_detail="Readiness transition persisted.")

    async def read_followup_receipt(
        self, demo_session_id: UUID, revision_id: UUID, action_id: UUID
    ) -> tuple[str, TraceStep]:
        return await self._execute(
            "reader",
            ReaderTemplate.FOLLOWUP_RECEIPT,
            "SELECT action_id, revision_id, owners, status, readiness_state "
            "FROM mart.sg_followup_receipts "
            f"WHERE demo_session_id = toUUID('{demo_session_id}') "
            f"AND revision_id = toUUID('{revision_id}') "
            f"AND action_id = toUUID('{action_id}') LIMIT 1",
            "Follow-up receipt retrieved through the reader MCP path.",
        )

    async def _execute(
        self, identity: str, template: StrEnum, query: str, public_detail: str
    ) -> tuple[str, TraceStep]:
        try:
            result = await self.run_query(identity, query)
        except Exception as error:
            raise McpBoundaryError("ClickHouse evidence path is unavailable.") from error
        return result, TraceStep(step=f"{identity}_mcp", status="confirmed", public_detail=public_detail)


def _require_scene_id(scene_id: str) -> None:
    if not _SCENE_ID.fullmatch(scene_id):
        raise ValueError("Unsupported scene identifier.")


def _quote(value: str) -> str:
    """Serialize an already-validated bounded value for one server-owned template."""

    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"
