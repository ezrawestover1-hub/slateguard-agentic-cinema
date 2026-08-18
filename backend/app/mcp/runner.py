"""Private stdio transport for the official ClickHouse MCP server.

The browser, agent, and API handlers never receive this object. Queries enter
only through named templates in ``boundary.py``.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from os import environ
import sys
from typing import Literal

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


McpIdentity = Literal["reader", "writer"]


class McpTransportError(RuntimeError):
    """Private transport failure; callers convert it to a public-safe error."""


@dataclass(frozen=True, slots=True)
class ClickHouseMcpRunner:
    """Start a least-privilege official MCP subprocess for each named request."""

    environment: Mapping[str, str] = field(repr=False)
    python_executable: str

    @classmethod
    def from_environment(cls) -> "ClickHouseMcpRunner":
        required = (
            "CLICKHOUSE_HOST",
            "CLICKHOUSE_PORT",
            "CLICKHOUSE_DATABASE",
            "CLICKHOUSE_SECURE",
            "CLICKHOUSE_VERIFY",
            "CLICKHOUSE_READER_USER",
            "CLICKHOUSE_READER_PASSWORD",
            "CLICKHOUSE_WRITER_USER",
            "CLICKHOUSE_WRITER_PASSWORD",
        )
        missing = tuple(name for name in required if not environ.get(name))
        if missing:
            raise McpTransportError("ClickHouse runtime configuration is incomplete.")
        return cls(
            environment=dict(environ),
            python_executable=environ.get("PYTHON_EXECUTABLE", sys.executable),
        )

    async def run_query(self, identity: McpIdentity, query: str) -> str:
        parameters = StdioServerParameters(
            command=self.python_executable,
            args=["-m", "mcp_clickhouse.main"],
            env=_server_environment(self.environment, identity),
        )
        try:
            async with stdio_client(parameters) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool("run_query", {"query": query})
                    if result.isError:
                        raise McpTransportError("ClickHouse MCP rejected a named query.")
                    return _result_text(result.content)
        except McpTransportError:
            raise
        except Exception as error:
            raise McpTransportError("ClickHouse MCP request failed.") from error


def _server_environment(parent: Mapping[str, str], identity: McpIdentity) -> dict[str, str]:
    """Pass only the selected identity and required ClickHouse settings to MCP."""

    prefix = "CLICKHOUSE_READER" if identity == "reader" else "CLICKHOUSE_WRITER"
    environment = {
        name: parent[name]
        for name in ("PATH", "SSL_CERT_FILE", "SSL_CERT_DIR")
        if parent.get(name)
    }
    environment.update(
        {
            "CLICKHOUSE_HOST": parent["CLICKHOUSE_HOST"],
            "CLICKHOUSE_PORT": parent["CLICKHOUSE_PORT"],
            "CLICKHOUSE_DATABASE": parent["CLICKHOUSE_DATABASE"],
            "CLICKHOUSE_SECURE": parent["CLICKHOUSE_SECURE"],
            "CLICKHOUSE_VERIFY": parent["CLICKHOUSE_VERIFY"],
            "CLICKHOUSE_USER": parent[f"{prefix}_USER"],
            "CLICKHOUSE_PASSWORD": parent[f"{prefix}_PASSWORD"],
            "CLICKHOUSE_ROLE": "sg_mcp_read_role" if identity == "reader" else "sg_mcp_write_role",
            "CLICKHOUSE_MCP_SERVER_TRANSPORT": "stdio",
            "CLICKHOUSE_ALLOW_DROP": "false",
            "CLICKHOUSE_ALLOW_WRITE_ACCESS": "true" if identity == "writer" else "false",
            "CLICKHOUSE_CONNECT_TIMEOUT": parent.get("CLICKHOUSE_CONNECT_TIMEOUT", "30"),
            "CLICKHOUSE_SEND_RECEIVE_TIMEOUT": parent.get("CLICKHOUSE_SEND_RECEIVE_TIMEOUT", "30"),
            "CLICKHOUSE_MCP_QUERY_TIMEOUT": parent.get("CLICKHOUSE_MCP_QUERY_TIMEOUT", "15"),
        }
    )
    return environment


def _result_text(content: object) -> str:
    """Extract only text blocks from the official MCP response object."""

    blocks = content if isinstance(content, list) else []
    text = "".join(str(getattr(block, "text", "") or "") for block in blocks).strip()
    if not text:
        raise McpTransportError("ClickHouse MCP returned no query result.")
    return text
