#!/usr/bin/env python3
"""Deploy and prove SlateGuard's real, evidence-bounded Change Packet agent.

This probe deliberately contains no ClickHouse tools or credentials. The product
backend retrieves and validates evidence through its least-privilege MCP boundary,
then sends only that bounded context to this agent. The agent can explain a packet;
it cannot change the deterministic readiness decision or write a follow-up.
"""

from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Mapping
from importlib.metadata import version
from typing import Literal

import vertexai
from google.adk.agents import Agent
from google.auth.exceptions import GoogleAuthError
from pydantic import BaseModel, Field, model_validator
from vertexai import agent_engines, types


PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
MODEL_LOCATION = os.environ.get("GOOGLE_GENAI_LOCATION", "us-central1")
RUNTIME_LOCATION = os.environ.get("SG_AGENT_RUNTIME_LOCATION", "us-central1")
STAGING_BUCKET = os.environ.get("SG_GCP_STAGING_BUCKET")
MODEL = "gemini-2.5-flash"
USER_ID = "slateguard-public-demo"

# Set before the ADK root agent is constructed. The deployed runtime receives
# the serialized Agent, while the backend invokes the managed endpoint later.
os.environ["GOOGLE_GENAI_USE_ENTERPRISE"] = "TRUE"


class ChangePacketNarrative(BaseModel):
    """The non-authoritative explanation returned to the SlateGuard backend."""

    status: Literal["ready", "review_required"]
    summary: str = Field(min_length=1, max_length=500)
    cited_evidence_ids: tuple[str, ...]
    recommended_owners: tuple[str, ...] = ()
    distinguishes_unknowns: bool

    @model_validator(mode="after")
    def requires_citations(self) -> "ChangePacketNarrative":
        if not self.cited_evidence_ids:
            raise ValueError("At least one supplied evidence ID must be cited.")
        return self


class ConfigurationError(RuntimeError):
    """Concise, secret-safe setup error."""


def require_project_id() -> str:
    if PROJECT_ID:
        return PROJECT_ID
    raise ConfigurationError("Missing GOOGLE_CLOUD_PROJECT.")


root_agent = Agent(
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


def create_app(project_id: str) -> agent_engines.AdkApp:
    """Create the portable ADK app using the same regional model endpoint as runtime."""

    os.environ["GOOGLE_CLOUD_LOCATION"] = MODEL_LOCATION
    vertexai.init(project=project_id, location=MODEL_LOCATION)
    return agent_engines.AdkApp(agent=root_agent)


def probe_input() -> dict[str, object]:
    """A production-shaped, evidence-bounded Scene 12 packet input."""

    return {
        "revision_id": "00000000-0000-0000-0000-000000000012",
        "scene_id": "scene-12",
        "previous_value": "blue jacket",
        "new_value": "black jacket",
        "evidence_ids": ["ev-dailies-11-blue", "ev-call-sheet-13", "ev-call-sheet-14"],
        "findings": [
            {"finding_type": "continuity_conflict", "evidence_ids": ["ev-dailies-11-blue"]},
            {
                "finding_type": "schedule_dependency",
                "evidence_ids": ["ev-call-sheet-13", "ev-call-sheet-14"],
            },
        ],
        "readiness": "At risk",
        "can_create_followup": True,
    }


def extract_final_text(event: object) -> str | None:
    """Read final content from local ADK or managed Agent Runtime streams."""

    if isinstance(event, Mapping):
        if not event.get("finish_reason"):
            return None
        content = event.get("content") or {}
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
    return "".join(getattr(part, "text", "") or "" for part in (content.parts or [])).strip() or None


async def run_probe(target: object, label: str) -> ChangePacketNarrative:
    grounded = probe_input()
    message = json.dumps(grounded, separators=(",", ":"))
    final_text: str | None = None
    async for event in target.async_stream_query(user_id=USER_ID, message=message):
        candidate = extract_final_text(event)
        if candidate:
            final_text = candidate
    if final_text is None:
        raise RuntimeError(f"{label}: no final model response received")

    packet = ChangePacketNarrative.model_validate_json(final_text)
    allowed_evidence = set(grounded["evidence_ids"])
    if not set(packet.cited_evidence_ids).issubset(allowed_evidence):
        raise RuntimeError(f"{label}: packet cited evidence outside its supplied context")
    if packet.status != "ready":
        raise RuntimeError(f"{label}: actionable packet unexpectedly requested review")
    if packet.recommended_owners != ("Wardrobe", "Assistant Director"):
        raise RuntimeError(f"{label}: packet recommended unapproved owners")
    if packet.distinguishes_unknowns is not True:
        raise RuntimeError(f"{label}: packet must distinguish supplied evidence from unknowns")

    print(
        json.dumps(
            {
                "probe": label,
                "project": require_project_id(),
                "model": MODEL,
                "model_location": MODEL_LOCATION,
                "status": packet.status,
                "cited_evidence_ids": packet.cited_evidence_ids,
                "recommended_owners": packet.recommended_owners,
                "distinguishes_unknowns": packet.distinguishes_unknowns,
            },
            indent=2,
        )
    )
    return packet


async def main() -> None:
    project_id = require_project_id()
    app = create_app(project_id)
    await run_probe(app, "local-change-packet")

    if os.environ.get("SG_DEPLOY") != "1":
        return
    if not STAGING_BUCKET:
        raise ConfigurationError("Missing SG_GCP_STAGING_BUCKET for Agent Runtime deployment.")

    client = vertexai.Client(project=project_id, location=RUNTIME_LOCATION)
    remote_agent = client.agent_engines.create(
        agent=app,
        config={
            "requirements": [
                "google-cloud-aiplatform[agent_engines,adk]"
                f"=={version('google-cloud-aiplatform')}",
                f"google-adk=={version('google-adk')}",
                f"cloudpickle=={version('cloudpickle')}",
                f"pydantic=={version('pydantic')}",
            ],
            "staging_bucket": STAGING_BUCKET,
            "identity_type": types.IdentityType.AGENT_IDENTITY,
        },
    )
    print(f"agent_runtime_resource={remote_agent.api_resource.name}")
    await run_probe(remote_agent, "deployed-change-packet")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (ConfigurationError, GoogleAuthError) as error:
        print(f"CONFIGURATION BLOCKED: {error}")
        raise SystemExit(2) from error
