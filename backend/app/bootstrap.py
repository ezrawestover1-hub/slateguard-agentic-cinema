"""Construct production services only when every required runtime boundary exists."""

from __future__ import annotations

from os import environ

from app.agents.gateway import GoogleChangePacketGateway
from app.agents.runtime import GoogleAgentRuntimeTarget, RuntimeConfigurationError
from app.mcp.boundary import ClickHouseMcpBoundary
from app.mcp.production_memory import ClickHouseFollowupMemory, ClickHouseProductionMemory
from app.mcp.runner import ClickHouseMcpRunner, McpTransportError
from app.services.demo_session import IdempotencyLedger, SessionSigner
from app.services.followup_flow import FollowupFlow
from app.services.revision_flow import RevisionFlow

from .main import ApplicationServices


def build_services_from_environment() -> ApplicationServices | None:
    """Return no services until all secrets/configuration are supplied securely."""

    session_secret = environ.get("SLATEGUARD_DEMO_SESSION_SECRET")
    if not session_secret:
        return None
    try:
        runner = ClickHouseMcpRunner.from_environment()
        target = GoogleAgentRuntimeTarget.from_environment()
    except (McpTransportError, RuntimeConfigurationError):
        return None

    boundary = ClickHouseMcpBoundary(runner.run_query)
    packet_gateway = GoogleChangePacketGateway(target)
    production_memory = ClickHouseProductionMemory(boundary)
    return ApplicationServices(
        signer=SessionSigner(session_secret.encode("utf-8")),
        revision_flow=RevisionFlow(
            memory=production_memory,
            packet_generator=packet_gateway.generate,
            ledger=IdempotencyLedger(),
        ),
        followup_flow=FollowupFlow(
            memory=ClickHouseFollowupMemory(boundary),
            ledger=IdempotencyLedger(),
        ),
        impact_pulse_reader=production_memory,
    )
