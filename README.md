# SlateGuard

SlateGuard is an evidence-first production change-control agent for a script supervisor. It turns one creative revision into a bounded, auditable decision loop:

```text
Scene 12 wardrobe revision
→ ClickHouse relevance pulse + official MCP write + evidence read
→ deterministic continuity and schedule findings
→ Gemini-grounded Change Packet
→ human-created follow-up
→ reader-verified shoot-readiness receipt
```

The public demo uses a self-authored fictional six-scene production. It is intentionally not a generic chat interface: the user can apply only the prepared `blue jacket → black jacket` Scene 12 revision, inspect evidence before acting, and create one accountable Wardrobe + Assistant Director follow-up.

## Live demo

SlateGuard is live at **https://sprint2---slateguard-vseh3ye7mq-uc.a.run.app**.

On 2026-08-18, Cloud Run revision `slateguard-00010-r2c` was exercised in the public browser: the Scene 12 revision persisted through the writer MCP path, curated evidence returned through the reader path, the grounded Change Packet validated, and the human-owned follow-up produced a reader-verified receipt. The live Impact Pulse returned four relevant evidence records and two affected scenes from its fixed reader-MCP aggregates. The app uses self-authored fictional data only; it does not include real production data.

## Why it matters

Creative changes are normal in production. What creates costly risk is an undocumented change reaching already-shot footage or tomorrow's call sheet. SlateGuard gives the supervisor a clear, source-backed blast radius and keeps the consequential action human-owned.

## Trust model

| Component | Responsibility | Cannot do |
| --- | --- | --- |
| Browser | Starts the supported revision and requests a follow-up. | Submit SQL, access credentials, select owners, or trigger arbitrary writes. |
| Reader MCP identity | Retrieves curated production evidence and verifies receipts. | Write or inspect unrestricted database records. |
| Writer MCP identity | Inserts validated append-only revision, impact, follow-up, and readiness events. | Read broadly, drop data, or accept browser/model SQL. |
| Deterministic rules | Identifies continuity/schedule findings and abstains on missing/contradictory sources. | Invent production evidence or delegate certainty to the model. |
| Gemini Change Packet agent | Explains supplied findings using only supplied evidence IDs. | Override readiness, invent citations, or create a follow-up. |
| Human supervisor | Creates the recommended follow-up. | Be replaced by the agent. |

## Architecture

```text
React Command Desk
        │ typed HTTP only
        ▼
FastAPI revision + follow-up flows
   ├── writer MCP ──► ClickHouse append-only events
   ├── reader MCP ◄── ClickHouse curated mart views
   ├── deterministic continuity/schedule rules
   └── Google ADK Change Packet gateway
                     │
                     ▼
          Gemini Enterprise Agent Runtime
```

The application launches two isolated instances of the official Python `mcp-clickhouse` server. The reader and writer have distinct identities and environments. No model or browser input becomes SQL.

## ClickHouse relevance pulse

Before the agent explains an impact, SlateGuard narrows its production memory to the active decision window: the established Scene 11 history, the Scene 12 revision, and the next scheduled dependencies. The public `/api/impact-pulse` route runs two fixed aggregate queries through the reader MCP identity and returns only four bounded counts—relevant evidence records, scene records in scope, affected scenes, and scheduled dependencies. Archive, unrelated, and unscheduled work never enters that decision context.

This is intentionally a relevance policy, not a made-up benchmark: the interface reports the real result of the curated queries and does not claim invented data volume or latency. The current Cloud Run revision exposes the live endpoint and has been browser-verified before the revision action.

## Judge proof map

| Demo moment | What should be visible | Evidence source |
| --- | --- | --- |
| Apply revision | `blue jacket → black jacket` begins a trace. | Typed revision API + writer MCP event. |
| Evidence before action | Scene 11 dailies and two upcoming call-sheet records. | Curated reader MCP queries. |
| Deterministic impact | One continuity conflict and two schedule dependencies. | Pure rules with stable evidence IDs. |
| Grounded explanation | Change Packet cites only returned records. | Schema-constrained Google ADK response. |
| Human decision | `Create follow-up` is the only consequential control. | Session-scoped endpoint and idempotency key. |
| Durable result | Action ID, owners, and `At risk → Follow-up created`. | Writer events followed by reader verification. |
| Runtime proof | Package version, sanitized IDs, write/read states—not raw SQL or secrets. | Public trace DTO. |

## Review and local development

**Fastest reviewer path:** open the [hosted SlateGuard demo](https://sprint2---slateguard-vseh3ye7mq-uc.a.run.app/). It uses self-authored fictional production data and requires no account.

The repository contains the frontend, backend, schema, tests, and deployment templates. The test suite and frontend build run without cloud credentials. A full local revision flow requires your own Google Cloud project plus a ClickHouse Cloud service with separate least-privilege reader and writer users; no project credentials are published in this repository.

### Verify the checked-in application

```sh
PYTHONPATH=backend .venv/bin/python -m unittest discover -s backend/tests -v
cd frontend && pnpm run build
```

### Run a local configured instance

1. Use Python 3.12+ and Node 20+ with pnpm enabled.
2. Copy `.env.example` to `.env` and supply **your own** Google Cloud and ClickHouse values. Never commit that file.
3. Follow the [Google ADK setup runbook](docs/sprint-0-google-runbook.md) and the [ClickHouse MCP setup runbook](docs/sprint-0-clickhouse-runbook.md) to create the constrained identities and validate the real reader → writer → reader path.
4. Build the frontend, then start the API with `PYTHONPATH=backend .venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8080`.

Open `http://127.0.0.1:8080/` after the server starts. Do not open `frontend/index.html` directly; the application uses typed HTTP API calls.

## Runtime verification

The project has recorded the following core proof points:

1. Official MCP reader → writer → reader behavior against ClickHouse Cloud, including denied permission checks.
2. Schema and fictional seed applied to ClickHouse and verified through the reader path.
3. Schema-valid Gemini Change Packet output from the deployed Agent Runtime.
4. A public Cloud Run Command Desk path showing revision persistence, evidence retrieval, and packet validation.
5. The live Impact Pulse: two curated reader-MCP aggregates, typed API coverage, and a browser-verified deployed command-desk state.

Before public-repository publication or Devpost handoff, run the release checks in [public repository readiness](docs/runbooks/public-repository-readiness.md). See [Sprint 0](docs/sprint-0.md), [build checklist](docs/hackathon-build/checklist.md), and [deployment gate](infra/DEPLOYMENT.md) for the supporting runtime detail.

The planned functional recording is in [demo script](docs/demo-script.md).

## License

MIT. See [LICENSE](LICENSE).
