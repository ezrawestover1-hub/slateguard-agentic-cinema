"""Lazy adapter for SlateGuard's deployed Google Agent Runtime resource."""

from __future__ import annotations

from collections.abc import AsyncIterator, Callable
from dataclasses import dataclass
from os import environ
from typing import Protocol


class ManagedQueryTarget(Protocol):
    def async_stream_query(self, *, user_id: str, message: str) -> AsyncIterator[object]: ...


class RuntimeConfigurationError(RuntimeError):
    """Raised without exposing deployment configuration to public callers."""


ClientFactory = Callable[..., object]


@dataclass(slots=True)
class GoogleAgentRuntimeTarget:
    """Resolve a managed agent lazily, so API startup never invokes a model."""

    project_id: str
    location: str
    resource_name: str
    client_factory: ClientFactory
    _target: ManagedQueryTarget | None = None
    _client: object | None = None

    @classmethod
    def from_environment(cls, client_factory: ClientFactory | None = None) -> "GoogleAgentRuntimeTarget":
        required = (
            "GOOGLE_CLOUD_PROJECT",
            "SG_AGENT_RUNTIME_LOCATION",
            "SG_CHANGE_PACKET_RUNTIME_RESOURCE",
        )
        missing = tuple(name for name in required if not environ.get(name))
        if missing:
            raise RuntimeConfigurationError("Google Change Packet runtime is not configured.")
        if client_factory is None:
            import vertexai

            client_factory = vertexai.Client
        return cls(
            project_id=environ["GOOGLE_CLOUD_PROJECT"],
            location=environ["SG_AGENT_RUNTIME_LOCATION"],
            resource_name=environ["SG_CHANGE_PACKET_RUNTIME_RESOURCE"],
            client_factory=client_factory,
        )

    async def async_stream_query(self, *, user_id: str, message: str) -> AsyncIterator[object]:
        target = self._resolve()
        async for event in target.async_stream_query(user_id=user_id, message=message):
            yield event

    def _resolve(self) -> ManagedQueryTarget:
        if self._target is None:
            client = self.client_factory(project=self.project_id, location=self.location)
            target = client.agent_engines.get(name=self.resource_name)  # type: ignore[attr-defined]
            # The managed target delegates async streaming to the Vertex client.
            # Retain that client so its aiohttp connector is not finalized between
            # resolving the target and consuming the response stream.
            self._client = client
            self._target = target
        return self._target
