"""The bounded revision-to-Change-Packet orchestration service."""

from __future__ import annotations

import asyncio
import hashlib
from collections.abc import Awaitable, Callable, Sequence
from dataclasses import dataclass
from uuid import UUID, uuid4

from pydantic import BaseModel

from app.agents.change_packet import (
    ChangePacketNarrative,
    GroundedPacketInput,
    deterministic_fallback,
    validate_agent_packet,
)
from app.domain.contracts import DependencyRecord, EvidenceRecord, RevisionRequest, RuleEvaluation
from app.mcp.boundary import TraceStep
from app.services.demo_session import IdempotencyLedger
from app.services.rules import evaluate_revision


class RevisionAnalysisResponse(BaseModel):
    revision_id: UUID
    change: RevisionRequest
    packet: ChangePacketNarrative
    evaluation: RuleEvaluation
    trace: tuple[TraceStep, ...]


class ProductionMemory:
    """Protocol-like narrow seam for real MCP adapters and deterministic test doubles."""

    async def append_revision(self, session_id: UUID, revision_id: UUID, idempotency_key: UUID, revision: RevisionRequest) -> TraceStep:  # pragma: no cover - interface
        raise NotImplementedError

    async def read_evidence(self, scene_id: str) -> Sequence[EvidenceRecord]:  # pragma: no cover - interface
        raise NotImplementedError

    async def read_dependencies(self, scene_id: str) -> Sequence[DependencyRecord]:  # pragma: no cover - interface
        raise NotImplementedError


PacketGenerator = Callable[[GroundedPacketInput], Awaitable[ChangePacketNarrative]]


@dataclass(slots=True)
class RevisionFlow:
    memory: ProductionMemory
    packet_generator: PacketGenerator
    ledger: IdempotencyLedger

    async def apply(
        self, session_id: UUID, request: RevisionRequest, idempotency_key: UUID
    ) -> RevisionAnalysisResponse:
        fingerprint = hashlib.sha256(request.model_dump_json().encode("utf-8")).hexdigest()
        existing = self.ledger.get_or_conflict(session_id, str(idempotency_key), fingerprint)
        if existing is not None:
            return existing  # type: ignore[return-value]

        revision_id = uuid4()
        write_trace = await self.memory.append_revision(session_id, revision_id, idempotency_key, request)
        evidence, dependencies = await asyncio.gather(
            self.memory.read_evidence(request.scene_id),
            self.memory.read_dependencies(request.scene_id),
        )
        evidence = tuple(evidence)
        dependencies = tuple(dependencies)
        evaluation = evaluate_revision(request, evidence, dependencies)
        retrieved_evidence_ids = tuple(record.evidence_id for record in evidence) + tuple(
            dependency.evidence_id for dependency in dependencies
        )
        evidence_ids = retrieved_evidence_ids if evaluation.can_create_followup else evaluation.review_evidence_ids
        grounded = GroundedPacketInput(
            revision_id=str(revision_id),
            scene_id=request.scene_id,
            fact_type=request.fact_type,
            previous_value=request.old_value,
            new_value=request.new_value,
            evidence_ids=evidence_ids,
            findings=evaluation.findings,
            readiness=evaluation.readiness,
            can_create_followup=evaluation.can_create_followup,
        )
        try:
            packet = validate_agent_packet(await self.packet_generator(grounded), grounded)
            agent_trace = TraceStep(step="change_packet_agent", status="confirmed", public_detail="Grounded Change Packet validated.")
        except Exception:
            packet = deterministic_fallback(grounded)
            agent_trace = TraceStep(step="change_packet_agent", status="fallback", public_detail="Factual Change Packet fallback applied.")
        response = RevisionAnalysisResponse(
            revision_id=revision_id,
            change=request,
            packet=packet,
            evaluation=evaluation,
            trace=(write_trace, TraceStep(step="reader_mcp", status="confirmed", public_detail="Evidence context retrieved."), agent_trace),
        )
        self.ledger.record_or_return(session_id, str(idempotency_key), fingerprint, response)
        return response
