from unittest import TestCase

from app.services.demo_session import (
    IdempotencyConflict,
    IdempotencyLedger,
    SessionSigner,
    SessionValidationError,
)


class DemoSessionTests(TestCase):
    def test_minted_session_verifies(self) -> None:
        signer = SessionSigner(b"test-secret", now=lambda: 1_000)
        token, expected = signer.mint(60)
        self.assertEqual(signer.verify(token), expected)

    def test_tampered_or_expired_session_fails_closed(self) -> None:
        signer = SessionSigner(b"test-secret", now=lambda: 1_000)
        token, _ = signer.mint(1)
        with self.assertRaises(SessionValidationError):
            signer.verify(f"{token}changed")
        expired_signer = SessionSigner(b"test-secret", now=lambda: 1_002)
        with self.assertRaises(SessionValidationError):
            expired_signer.verify(token)

    def test_idempotency_is_scoped_to_session_and_payload(self) -> None:
        signer = SessionSigner(b"test-secret", now=lambda: 1_000)
        _, first = signer.mint()
        _, second = signer.mint()
        ledger = IdempotencyLedger()
        original = {"action_id": "one"}
        self.assertIs(ledger.record_or_return(first.session_id, "request-1", "revision-v1", original), original)
        self.assertIs(ledger.record_or_return(first.session_id, "request-1", "revision-v1", {"action_id": "ignored"}), original)
        self.assertEqual(ledger.record_or_return(second.session_id, "request-1", "revision-v1", {"action_id": "two"}), {"action_id": "two"})
        with self.assertRaises(IdempotencyConflict):
            ledger.record_or_return(first.session_id, "request-1", "different-payload", {})
