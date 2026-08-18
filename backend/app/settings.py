"""Typed, fail-closed runtime configuration for the SlateGuard API."""

from __future__ import annotations

from dataclasses import dataclass
from os import getenv
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    """Non-secret settings required for each runtime mode.

    Secrets deliberately stay outside this object until the MCP adapters are added.
    This prevents accidental disclosure through startup logs or health responses.
    """

    environment: str
    static_dir: Path
    configured: bool

    @classmethod
    def from_environment(cls) -> "Settings":
        project_root = Path(__file__).resolve().parents[2]
        static_dir = Path(getenv("SLATEGUARD_STATIC_DIR", project_root / "frontend" / "dist"))
        required_later = ("GOOGLE_CLOUD_PROJECT", "CLICKHOUSE_HOST", "CLICKHOUSE_DATABASE")
        configured = all(getenv(key) for key in required_later)
        return cls(
            environment=getenv("SLATEGUARD_ENV", "development"),
            static_dir=static_dir,
            configured=configured,
        )
