"""Google ADK gateway for SlateGuard's schema-constrained Change Packet agent."""

from __future__ import annotations

import json
import logging
from collections.abc import AsyncIterator, Callable, Mapping
from dataclasses import dataclass
from typing import Protocol

from google.adk.agents import Agent

from app.agents.change_packet import ChangePacketNarrative, GroundedPacketInput


MODEL = "gemini-2.5-flash"
USER_ID = "slateguard-public-demo"
logger = logging.getLogger(__name__)


class StreamTarget(Protocol):
    def async_stream_query(self, *, user_id: str, message: str) -> AsyncIterator[object]: ...


class AgentGatewayError(RuntimeError):
    """Non-diagnostic failure for callers; the flow uses deterministic fallback."""


def create_change_packet_agent() -> Agent:
    return Agent(
        name="slateguard_change_packet",
        model=MODEL,
        instruction=(
            "Produce a concise SlateGuard Change Packet from the supplied JSON only. "
            "Cite only evidence_ids supplied in the input. Preserve the supplied readiness "
            "as a factual label in the summary, but do not treat it as the response status. "
            "When can_create_followup is true, status must be ready and recommend exactly "
            "Wardrobe and Assistant Director. When it is false, status must be review_required "
            "and recommend no owners. Always set distinguishes_unknowns to true because the "
            "packet must clearly separate supplied evidence from unknowns. Do not make claims "
            "outside the JSON. Return only the response schema."
        ),
        output_schema=ChangePacketNarrative,
        output_key="change_packet",
    )


@dataclass(frozen=True, slots=True)
class GoogleChangePacketGateway:
    target: StreamTarget

    async def generate(self, grounded: GroundedPacketInput) -> ChangePacketNarrative:
        prompt = json.dumps(grounded.model_dump(mode="json"), separators=(",", ":"))
        final_text: str | None = None
        try:
            async for event in self.target.async_stream_query(user_id=USER_ID, message=prompt):
                candidate = _final_text(event)
                if candidate:
                    final_text = candidate
            if final_text is None:
                raise AgentGatewayError("No final agent response.")
            return ChangePacketNarrative.model_validate_json(final_text)
        except Exception as error:
            if isinstance(error, AgentGatewayError):
                raise
            logger.exception("Google Change Packet runtime request failed.")
            raise AgentGatewayError("Google Change Packet path is unavailable.") from error


def _final_text(event: object) -> str | None:
    """Read final response text without binding the app to streaming event internals."""

    # Agent Runtime can stream mapping-shaped events while the local ADK path
    # uses objects. Accept both formats; neither shape leaks to the browser.
    if isinstance(event, Mapping):
        if not event.get("finish_reason"):
            return None
        content = event.get("content")
        parts = content.get("parts") if isinstance(content, Mapping) else None
        text = "".join(
            str(part.get("text") or "")
            for part in (parts or [])
            if isinstance(part, Mapping)
        ).strip()
        return text or None

    is_final = getattr(event, "is_final_response", None)
    content = getattr(event, "content", None)
    if not callable(is_final) or not is_final() or content is None:
        return None
    parts = getattr(content, "parts", None) or []
    text = "".join(getattr(part, "text", "") or "" for part in parts).strip()
    return text or None
