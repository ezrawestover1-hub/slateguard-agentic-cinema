#!/usr/bin/env python3
"""Run fixed, credential-safe Sprint 0 checks through official mcp-clickhouse.

This probe intentionally exposes no arbitrary SQL input. It starts the official server
as a stdio child process and uses fixed read/write statements to verify that the
least-privilege ClickHouse roles work as designed.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
import uuid
from collections.abc import Mapping

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SMOKE_TABLE = "mcp_smoke_events"


class ConfigurationError(RuntimeError):
    """Raised when a required local-only configuration value is absent."""


class ToolExecutionError(RuntimeError):
    """Raised when an MCP server returns a tool-level error result."""


def require_environment(names: tuple[str, ...]) -> None:
    missing = [name for name in names if not os.environ.get(name)]
    if missing:
        joined = ", ".join(missing)
        raise ConfigurationError(
            f"Missing required environment variables: {joined}. "
            "Copy .env.example to a local .env file, set values outside Git, "
            "then rerun this probe."
        )


def server_environment(mode: str) -> dict[str, str]:
    """Build a distinct reader or writer server environment without logging secrets."""

    common = (
        "CLICKHOUSE_HOST",
        "CLICKHOUSE_PORT",
        "CLICKHOUSE_DATABASE",
        "CLICKHOUSE_SECURE",
        "CLICKHOUSE_VERIFY",
    )
    credential_prefix = "CLICKHOUSE_READER" if mode == "reader" else "CLICKHOUSE_WRITER"
    require_environment(common + (f"{credential_prefix}_USER", f"{credential_prefix}_PASSWORD"))

    # Start from a minimal inherited environment rather than copying the parent
    # process. This prevents unrelated credentials/configuration from reaching
    # either MCP child; ClickHouse configuration is added explicitly below.
    environment = {
        name: os.environ[name]
        for name in ("PATH", "SSL_CERT_FILE", "SSL_CERT_DIR")
        if os.environ.get(name)
    }
    environment.update(
        {
            "CLICKHOUSE_USER": os.environ[f"{credential_prefix}_USER"],
            "CLICKHOUSE_PASSWORD": os.environ[f"{credential_prefix}_PASSWORD"],
            "CLICKHOUSE_ROLE": (
                "sg_mcp_read_role" if mode == "reader" else "sg_mcp_write_role"
            ),
            "CLICKHOUSE_MCP_SERVER_TRANSPORT": "stdio",
            "CLICKHOUSE_ALLOW_DROP": "false",
            "CLICKHOUSE_ALLOW_WRITE_ACCESS": "true" if mode == "writer" else "false",
            "CLICKHOUSE_CONNECT_TIMEOUT": os.environ.get("CLICKHOUSE_CONNECT_TIMEOUT", "30"),
            "CLICKHOUSE_SEND_RECEIVE_TIMEOUT": os.environ.get(
                "CLICKHOUSE_SEND_RECEIVE_TIMEOUT", "30"
            ),
            "CLICKHOUSE_MCP_QUERY_TIMEOUT": os.environ.get(
                "CLICKHOUSE_MCP_QUERY_TIMEOUT", "15"
            ),
        }
    )
    return environment


async def run_query(mode: str, query: str) -> str:
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "mcp_clickhouse.main"],
        env=server_environment(mode),
    )

    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool("run_query", {"query": query})
            if result.isError:
                raise ToolExecutionError(str(result.content))
            return str(result.content)


async def expect_success(mode: str, query: str, label: str) -> str:
    result = await run_query(mode, query)
    print(f"PASS {label}: {result}")
    return result


async def expect_denied(mode: str, query: str, label: str) -> None:
    denied = False
    try:
        result = await run_query(mode, query)
    except* ToolExecutionError:
        # MCP's stdio transport can wrap a tool-level access denial inside an
        # ExceptionGroup while it closes its task group. Treat that shape the
        # same as the direct, expected denial without masking unrelated errors.
        denied = True

    if denied:
        print(f"PASS {label}: denied as expected")
        return

    raise RuntimeError(f"{label} unexpectedly succeeded: {result}")


async def run_all() -> None:
    event_id = uuid.uuid4()
    reader_query = f"SELECT count() AS event_count FROM {SMOKE_TABLE}"
    writer_query = (
        f"INSERT INTO {SMOKE_TABLE} (event_id, event_kind, actor, created_at) VALUES "
        f"('{event_id}', 'sprint0_mcp_write', 'backend_smoke', now64(3))"
    )
    verification_query = (
        f"SELECT event_id, event_kind, actor, created_at FROM {SMOKE_TABLE} "
        f"WHERE event_id = toUUID('{event_id}') ORDER BY created_at DESC LIMIT 1"
    )

    await expect_success("reader", reader_query, "reader connection")
    await expect_success("writer", writer_query, "writer event")
    await expect_success("reader", verification_query, "reader verification")
    await expect_denied("reader", writer_query, "reader write guard")
    await expect_denied("writer", reader_query, "writer read guard")


async def main_async(mode: str) -> None:
    if mode == "all":
        await run_all()
        return
    if mode == "reader":
        await expect_success(
            "reader",
            f"SELECT count() AS event_count FROM {SMOKE_TABLE}",
            "reader connection",
        )
        return
    raise ValueError(f"Unsupported mode: {mode}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run fixed Sprint 0 MCP/ClickHouse capability checks."
    )
    parser.add_argument(
        "--mode",
        choices=("all", "reader"),
        default="all",
        help="Run all least-privilege checks, or only the reader connectivity check.",
    )
    arguments = parser.parse_args()
    try:
        asyncio.run(main_async(arguments.mode))
    except ConfigurationError as error:
        print(f"CONFIGURATION BLOCKED: {error}", file=sys.stderr)
        raise SystemExit(2) from error


if __name__ == "__main__":
    main()
