"""Human-owned follow-up creation and reader-verified decision receipts."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from uuid import UUID, uuid4

from pydantic import BaseModel

from app.mcp.boundary import TraceStep
from app.services.demo_session import IdempotencyLedger


class FollowupNotAllowed(ValueError):
    """The revision lacks a stored, actionable deterministic impact."""


class DecisionReceipt(BaseModel):
    action_id: UUID
    revision_id: UUID
    owners: tuple[str, str] = ("Wardrobe", "Assistant Director")
    status: str = "Follow-up created"
    readiness_from: str = "At risk"
    readiness_to: str = "Follow-up created"
    evidence_ids: tuple[str, ...]
    trace: tuple[TraceStep, ...]


class FollowupMemory:
    """Narrow seam whose production implementation uses writer/readers MCP paths."""

    async def is_actionable(self, session_id: UUID, revision_id: UUID) -> bool:  # pragma: no cover - interface
        raise NotImplementedError

    async def append_followup(self, session_id: UUID, action_id: UUID, revision_id: UUID) -> TraceStep:  # pragma: no cover - interface
        raise NotImplementedError

    async def append_readiness(self, session_id: UUID, revision_id: UUID) -> TraceStep:  # pragma: no cover - interface
        raise NotImplementedError

    async def read_receipt_evidence(self, session_id: UUID, revision_id: UUID, action_id: UUID) -> tuple[str, ...]:  # pragma: no cover - interface
        raise NotImplementedError


@dataclass(slots=True)
class FollowupFlow:
    memory: FollowupMemory
    ledger: IdempotencyLedger

    async def create(self, session_id: UUID, revision_id: UUID, idempotency_key: UUID) -> DecisionReceipt:
        fingerprint = hashlib.sha256(f"followup:{revision_id}".encode("utf-8")).hexdigest()
        existing = self.ledger.get_or_conflict(session_id, str(idempotency_key), fingerprint)
        if existing is not None:
            return existing  # type: ignore[return-value]
        if not await self.memory.is_actionable(session_id, revision_id):
            raise FollowupNotAllowed("Follow-up requires an actionable stored impact.")
        action_id = uuid4()
        followup_trace = await self.memory.append_followup(session_id, action_id, revision_id)
        readiness_trace = await self.memory.append_readiness(session_id, revision_id)
        evidence_ids = await self.memory.read_receipt_evidence(session_id, revision_id, action_id)
        receipt = DecisionReceipt(
            action_id=action_id,
            revision_id=revision_id,
            evidence_ids=evidence_ids,
            trace=(followup_trace, readiness_trace, TraceStep(step="reader_mcp", status="confirmed", public_detail="Persisted follow-up and readiness verified.")),
        )
        self.ledger.record_or_return(session_id, str(idempotency_key), fingerprint, receipt)
        return receipt
