"""Signed, short-lived demo sessions and session-scoped idempotency."""

from __future__ import annotations

import base64
import hashlib
import hmac
import time
from dataclasses import dataclass, field
from uuid import UUID, uuid4


class SessionValidationError(ValueError):
    """Raised without disclosing whether a token was malformed, altered, or expired."""


class IdempotencyConflict(ValueError):
    """A key may not be reused for a different request in the same demo session."""


@dataclass(frozen=True, slots=True)
class DemoSession:
    session_id: UUID
    expires_at: int


@dataclass(slots=True)
class SessionSigner:
    secret: bytes
    now: callable = time.time

    def mint(self, lifetime_seconds: int = 1800) -> tuple[str, DemoSession]:
        session = DemoSession(uuid4(), int(self.now()) + lifetime_seconds)
        payload = f"{session.session_id}.{session.expires_at}"
        return f"{payload}.{self._signature(payload)}", session

    def verify(self, token: str) -> DemoSession:
        try:
            session_id_text, expiry_text, supplied_signature = token.split(".")
            payload = f"{session_id_text}.{expiry_text}"
            session = DemoSession(UUID(session_id_text), int(expiry_text))
        except (TypeError, ValueError):
            raise SessionValidationError("Invalid demo session.") from None
        if not hmac.compare_digest(self._signature(payload), supplied_signature) or session.expires_at <= int(self.now()):
            raise SessionValidationError("Invalid demo session.")
        return session

    def _signature(self, payload: str) -> str:
        digest = hmac.new(self.secret, payload.encode("utf-8"), hashlib.sha256).digest()
        return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


@dataclass(slots=True)
class IdempotencyLedger:
    """Temporary in-process seam; the real implementation is ClickHouse-backed."""

    _records: dict[tuple[UUID, str], tuple[str, object]] = field(default_factory=dict)

    def get_or_conflict(self, session_id: UUID, key: str, fingerprint: str) -> object | None:
        existing = self._records.get((session_id, key))
        if existing is None:
            return None
        existing_fingerprint, existing_result = existing
        if existing_fingerprint != fingerprint:
            raise IdempotencyConflict("Idempotency key cannot be reused for another request.")
        return existing_result

    def record_or_return(self, session_id: UUID, key: str, fingerprint: str, result: object) -> object:
        lookup = (session_id, key)
        existing = self._records.get(lookup)
        if existing is None:
            self._records[lookup] = (fingerprint, result)
            return result
        existing_fingerprint, existing_result = existing
        if existing_fingerprint != fingerprint:
            raise IdempotencyConflict("Idempotency key cannot be reused for another request.")
        return existing_result
