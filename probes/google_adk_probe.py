#!/usr/bin/env python3
"""Prove a minimal, permitted Google ADK structured-output path for Sprint 0.

The local proof has no MCP tools by design. It validates the Google-only agent runtime
first; ClickHouse MCP is proved by the separate, least-privilege probe.
"""

from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Mapping
from importlib.metadata import version
from typing import Literal

import vertexai
from google.auth.exceptions import GoogleAuthError
from google.adk.agents import Agent
from pydantic import BaseModel, Field
from vertexai import agent_engines, types


PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
MODEL_LOCATION = os.environ.get("GOOGLE_GENAI_LOCATION", "us-central1")
RUNTIME_LOCATION = os.environ.get("SG_AGENT_RUNTIME_LOCATION", "us-central1")
STAGING_BUCKET = os.environ.get("SG_GCP_STAGING_BUCKET")
USER_ID = "sprint0-proof-user"
MODEL = "gemini-2.5-flash"

# This is a Google Cloud-only probe. Set the ADK backend before the root agent
# is constructed rather than trusting a shell-level flag that package startup
# can normalize while importing the agent framework.
os.environ["GOOGLE_GENAI_USE_ENTERPRISE"] = "TRUE"


class FactChange(BaseModel):
    """The smallest useful typed result for the Google-only Sprint 0 proof."""

    scene_number: str = Field(description="Scene number without the word 'Scene'.")
    fact_type: Literal["wardrobe"] = Field(
        description="The production-fact category changed."
    )
    previous_value: str = Field(description="The prior stated value.")
    new_value: str = Field(description="The replacement stated value.")
    review_required: bool = Field(
        description="Must be true: a human must confirm production impact."
    )


class ConfigurationError(RuntimeError):
    """Raised when the local-only Google Cloud configuration is incomplete."""


def require_project_id() -> str:
    """Return the selected project or raise a concise, secret-safe setup error."""

    if PROJECT_ID:
        return PROJECT_ID
    raise ConfigurationError(
        "Missing GOOGLE_CLOUD_PROJECT. Copy .env.example to a local .env file, "
        "set the isolated Google Cloud project ID outside Git, then rerun this probe."
    )


root_agent = Agent(
    name="slateguard_change_extractor",
    model=MODEL,
    instruction=(
        "Extract exactly one production-fact revision from the user's message. "
        "Use only facts explicitly stated in the message; never invent scene data. "
        "Set review_required to true because every production change needs human review. "
        "Return only the JSON object required by the response schema."
    ),
    output_schema=FactChange,
    output_key="fact_change",
)


def create_app(project_id: str) -> agent_engines.AdkApp:
    """Initialize Vertex AI before constructing the locally executed ADK app."""

    # Gemini 2.5 Flash is available in the same us-central1 region as the
    # managed Agent Runtime deployment, avoiding cross-endpoint model routing.
    os.environ["GOOGLE_CLOUD_LOCATION"] = MODEL_LOCATION
    vertexai.init(project=project_id, location=MODEL_LOCATION)
    return agent_engines.AdkApp(agent=root_agent)


def extract_final_text(event: object) -> str | None:
    """Return final textual content without relying on non-final streamed events."""

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

    if not event.is_final_response() or not event.content:
        return None
    parts = event.content.parts or []
    text = "".join(part.text or "" for part in parts).strip()
    return text or None


async def run_probe(target: object, label: str) -> FactChange:
    prompt = "Scene 12 wardrobe changes from blue jacket to black jacket."
    final_text = None

    async for event in target.async_stream_query(user_id=USER_ID, message=prompt):
        candidate = extract_final_text(event)
        if candidate:
            final_text = candidate

    if final_text is None:
        raise RuntimeError(f"{label}: no final model response received")

    result = FactChange.model_validate_json(final_text)
    if result.review_required is not True:
        raise RuntimeError(f"{label}: review_required must be true")
    print(
        json.dumps(
            {
                "probe": label,
                "project": require_project_id(),
                "model_location": MODEL_LOCATION,
                "model": MODEL,
                "raw_response": final_text,
                "validated": result.model_dump(),
            },
            indent=2,
        )
    )
    return result


async def main() -> None:
    """Run locally, then optionally deploy the identical agent to Agent Runtime."""

    project_id = require_project_id()
    app = create_app(project_id)
    await run_probe(app, "local-adk")

    if os.environ.get("SG_DEPLOY") != "1":
        return

    if not STAGING_BUCKET:
        raise RuntimeError(
            "Set SG_GCP_STAGING_BUCKET=gs://... before deploying the Agent Runtime object."
        )

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
    await run_probe(remote_agent, "deployed-agent-runtime")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (ConfigurationError, GoogleAuthError) as error:
        print(f"CONFIGURATION BLOCKED: {error}")
        raise SystemExit(2) from error
