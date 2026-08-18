"""HTTP boundary for SlateGuard.

Only dependency-safe endpoints live here until the ClickHouse and Agent Runtime
proofs have passed. Health responses are intentionally non-diagnostic.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
from uuid import UUID

from fastapi import FastAPI, Header, HTTPException, Request, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .domain.contracts import ImpactPulse, RevisionRequest
from .mcp.boundary import McpBoundaryError
from .mcp.runner import McpTransportError
from .services.demo_session import DemoSession, IdempotencyConflict, SessionSigner, SessionValidationError
from .services.followup_flow import FollowupFlow, FollowupNotAllowed
from .services.revision_flow import RevisionFlow
from .settings import Settings


class ImpactPulseReader(Protocol):
    async def read_impact_pulse(self) -> ImpactPulse: ...


@dataclass(frozen=True, slots=True)
class ApplicationServices:
    signer: SessionSigner
    revision_flow: RevisionFlow
    followup_flow: FollowupFlow | None = None
    impact_pulse_reader: ImpactPulseReader | None = None


def create_app(settings: Settings | None = None, services: ApplicationServices | None = None) -> FastAPI:
    runtime_settings = settings or Settings.from_environment()
    runtime_services = services
    if runtime_services is None:
        from .bootstrap import build_services_from_environment

        runtime_services = build_services_from_environment()
    app = FastAPI(title="SlateGuard", version="0.1.0", docs_url=None, redoc_url=None)
    app.state.settings = runtime_settings

    # The document shell is served explicitly below so it can retain the
    # frontend-pending response during backend-only development. Vite's
    # fingerprinted production assets need their own mounted path in the
    # deployed runtime.
    assets_dir = Path(runtime_settings.static_dir) / "assets"
    if assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="frontend-assets")

    @app.get("/healthz", include_in_schema=False)
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/api/runtime-status", include_in_schema=False)
    async def runtime_status() -> JSONResponse:
        # Publicly useful but deliberately avoids exposing dependency names,
        # environment values, or configuration details.
        state = "ready" if runtime_services is not None else "configuration_pending"
        return JSONResponse({"state": state})

    @app.get("/api/impact-pulse", include_in_schema=False)
    async def impact_pulse() -> JSONResponse:
        if runtime_services is None or runtime_services.impact_pulse_reader is None:
            raise HTTPException(status_code=503, detail="Runtime configuration is pending.")
        try:
            pulse = await runtime_services.impact_pulse_reader.read_impact_pulse()
        except (McpBoundaryError, McpTransportError):
            raise HTTPException(status_code=503, detail="Required runtime evidence is temporarily unavailable.") from None
        return JSONResponse(pulse.model_dump(mode="json"))

    @app.post("/api/demo/reset", include_in_schema=False)
    async def reset_demo(response: Response) -> dict[str, str]:
        if runtime_services is None:
            raise HTTPException(status_code=503, detail="Runtime configuration is pending.")
        token, session = runtime_services.signer.mint()
        response.set_cookie(
            key="sg_demo_session",
            value=token,
            httponly=True,
            samesite="lax",
            secure=runtime_settings.environment == "production",
            max_age=session.expires_at - int(runtime_services.signer.now()),
        )
        return {"state": "ready", "session_id": str(session.session_id)}

    @app.post("/api/revisions", include_in_schema=False)
    async def apply_revision(
        revision: RevisionRequest,
        request: Request,
        idempotency_key: str = Header(alias="Idempotency-Key"),
    ) -> JSONResponse:
        if runtime_services is None:
            raise HTTPException(status_code=503, detail="Runtime configuration is pending.")
        try:
            session = _verified_session(runtime_services.signer, request.cookies.get("sg_demo_session"))
            result = await runtime_services.revision_flow.apply(session.session_id, revision, UUID(idempotency_key))
        except IdempotencyConflict:
            raise HTTPException(status_code=409, detail="Idempotency key conflicts with an existing request.") from None
        except (McpBoundaryError, McpTransportError):
            raise HTTPException(status_code=503, detail="Required runtime evidence is temporarily unavailable.") from None
        except (SessionValidationError, ValueError):
            raise HTTPException(status_code=422, detail="Invalid demo session or request.") from None
        return JSONResponse(result.model_dump(mode="json"))

    @app.post("/api/revisions/{revision_id}/follow-up", include_in_schema=False)
    async def create_followup(
        revision_id: UUID,
        request: Request,
        idempotency_key: str = Header(alias="Idempotency-Key"),
    ) -> JSONResponse:
        if runtime_services is None or runtime_services.followup_flow is None:
            raise HTTPException(status_code=503, detail="Runtime configuration is pending.")
        try:
            session = _verified_session(runtime_services.signer, request.cookies.get("sg_demo_session"))
            receipt = await runtime_services.followup_flow.create(session.session_id, revision_id, UUID(idempotency_key))
        except FollowupNotAllowed:
            raise HTTPException(status_code=409, detail="This revision cannot create a follow-up.") from None
        except IdempotencyConflict:
            raise HTTPException(status_code=409, detail="Idempotency key conflicts with an existing request.") from None
        except (McpBoundaryError, McpTransportError):
            raise HTTPException(status_code=503, detail="Required runtime evidence is temporarily unavailable.") from None
        except (SessionValidationError, ValueError):
            raise HTTPException(status_code=422, detail="Invalid demo session or request.") from None
        return JSONResponse(receipt.model_dump(mode="json"))

    @app.get("/", include_in_schema=False, response_model=None)
    async def index() -> FileResponse | JSONResponse:
        index_file = runtime_settings.static_dir / "index.html"
        if index_file.is_file():
            return FileResponse(index_file)
        return JSONResponse(
            {
                "state": "frontend_pending",
                "message": "SlateGuard interface is not built in this runtime yet.",
            },
            status_code=503,
        )

    return app


app = create_app()


def _verified_session(signer: SessionSigner, token: str | None) -> DemoSession:
    if not token:
        raise SessionValidationError("Invalid demo session.")
    return signer.verify(token)
