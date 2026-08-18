# Sprint 0 — access and runtime-proof setup

## Objective

Prepare a secure local project foundation and prove that the required Google and ClickHouse paths can run for real before product or UI work begins.

## Completed

- [x] Contest strategy, architecture, resource plan, and implementation blueprint locked.
- [x] Local Git repository initialized on the main branch.
- [x] Secret-safe .gitignore and .env.example created.
- [x] Organizer Google Cloud credit request submitted.
- [x] $450 in Google Cloud credit confirmed by the builder.
- [x] Locally validate the pinned Python 3.12 toolchain: mcp-clickhouse 0.4.1, Google Cloud AI Platform 1.164.0, Google ADK 2.7.0, Google Gen AI 2.18.1, and Pydantic 2.13.4.
- [x] Compile both probes, validate their imports/schema construction, and make both fail closed when required cloud configuration is absent.
- [x] Create isolated GCP project `slateguard-agentic-cinema-2026`, attach the existing approved billing/credit account, and create a $300 monthly budget alert.

## Human access gates

- [x] Create or select the isolated Google Cloud project; attach billing/credit and grant the required project access.
- [x] Create the real ClickHouse Cloud service and obtain host, database, and least-privilege reader/writer credentials.
- [ ] Create the remote GitHub repository when ready to publish the local repository.

## Technical gates

- [x] Pin official mcp-clickhouse 0.4.1; use Python 3.12 because the server requires Python 3.10 or newer.
- [x] Implement the selected deployed model path: gemini-2.5-flash in Vertex AI us-central1, matching the managed Agent Runtime region.
- [x] Run one real reader query through mcp-clickhouse against the ClickHouse Cloud service.
- [x] Run one controlled writer event through mcp-clickhouse, then verify it with the reader path.
- [x] Run one permitted Gemini / Google ADK structured-output call using the selected GCP project.
- [x] Demonstrate both paths from a deployable process, not only an interactive local shell.

## Local verification record — 2026-08-14

- The bundled Python 3.12 environment installed the pinned toolchain successfully; `pip check` and Python compilation both pass.
- The Google probe constructs its `FactChange` structured-output schema and `AdkApp` without a live request once a project identifier is supplied.
- The ClickHouse probe imports the official `mcp-clickhouse` server and uses two separately configured stdio child-process identities.
- With no credentials present, both probes stop with exit code 2 and a concise setup message. That is intentional safety behavior, not a real-runtime proof.
- No Google Cloud resource, Gemini request, ClickHouse service, or billable managed runtime has been created during this local verification.

## Cloud provisioning record — 2026-08-15

- The isolated project `slateguard-agentic-cinema-2026` was created in the signed-in Google Cloud account.
- The existing credit-backed billing account is linked to the project; the console showed a $0.00 SlateGuard project total at creation time.
- A $300 monthly budget alert was created. It is an alert, not a hard spending cap.
- The Google Cloud Console API-library page returned a load failure before any required API was enabled. No API enablement, service-account change, Secret Manager secret, Cloud Run service, Agent Runtime resource, or ClickHouse service was created after the failure.
- Cloud Shell was started in the new project, but its `gcloud` session has no active authenticated account. The allowlisted enablement command therefore failed before changing any API state. The next access action is an explicit `gcloud auth login`; do not retry the enable command until that login succeeds.
- Cloud Shell was subsequently authenticated to the project owner and the fixed allowlist completed successfully: Vertex AI, Cloud Run, Artifact Registry, Secret Manager, Cloud Storage, Cloud Logging, Cloud Monitoring, Cloud Resource Manager, Service Usage, Telemetry, and Cloud Trace APIs are enabled. No runtime service, service account, secret, Agent Runtime, or Cloud Run deployment has been created yet.
- Attempted ClickHouse Cloud Google sign-in returned a ClickHouse session/cookie error immediately after Google consent. No ClickHouse organization, service, database, credential, or billable resource was created. Do not represent the ClickHouse runtime proof as complete; resume only after a clean ClickHouse console session is available.
- The Google Cloud Marketplace page now confirms that the ClickHouse Cloud subscription is **pending ClickHouse approval**. The Marketplace signup handoff was invoked once, but it remained on the pending subscription page rather than opening a service console. No retry loop was run and no database, credential, or ClickHouse workload has been created. The next external-state signal is ClickHouse activation/approval.

## ClickHouse runtime-proof record — 2026-08-16

- The real `slateguard-mcp` ClickHouse Cloud service is running in GCP `us-central1`; its non-secret HTTPS endpoint was used on port 8443.
- Two isolated users were created with separate role assignments: `sg_mcp_read` can use only curated evidence views and the smoke table; `sg_mcp_write` can append only to the named event tables and the smoke table. Credentials are stored only in the ignored local `.env` file with owner-only permissions.
- The official Python `mcp-clickhouse==0.4.1` server completed a real stdio proof against ClickHouse Cloud (server version `26.2.1.558`): reader query passed, writer append passed, reader verification passed, reader write was denied, and writer broad read was denied.
- The proof harness was corrected to recognize the MCP client's grouped tool-error shape for expected permission denials. It was Python-compiled and then rerun successfully end to end.
- The Sprint 0 proof uses its isolated smoke table. The app's curated production views require a separate admin-only schema/role setup in `docs/sprint-1-clickhouse-production-setup.md`; the reader correctly failed closed rather than receiving underlying-table access.
- On 2026-08-17, the production schema, six-scene seed, and two `SQL SECURITY DEFINER` curated views were verified in the service. The reader role was granted only those two views; the writer role was granted only `INSERT` on the four append-only event tables.
- The application’s own MCP runner then retrieved all four evidence records and both scheduled dependencies, appended a typed Scene 12 revision, denied a reader write, and denied a writer broad read. The real revision flow produced the deterministic continuity conflict, two schedule dependencies, and an `At risk` readiness result. This proves the ClickHouse portion of the key path; the hosted API and human follow-up receipt are still separate build gates.
- The next Sprint 1 receipt proof added two security-definer views for revision actionability and follow-up receipts, then granted the reader role only `SELECT` on those views. A real session completed revision → reader actionability check → writer follow-up → writer readiness event → reader-confirmed receipt. The verified receipt named Wardrobe and Assistant Director, transitioned readiness to `Follow-up created`, and recovered the Scene 11 dailies plus both scheduled call-sheet evidence IDs.

## Google ADK runtime-proof record — 2026-08-16

- Cloud Shell was authenticated to `slateguard-agentic-cinema-2026`; the uniform-access staging bucket `gs://slateguard-agentic-cinema-2026-agent-runtime-staging` was created in `us-central1`.
- The initial `gemini-3.5-flash` deployment correctly failed at invocation because that publisher model was unavailable from the regional `us-central1` endpoint. The first failed Agent Runtime resource was force-deleted; it is not part of the live proof.
- The selected implementation now uses `gemini-2.5-flash` in `us-central1`, so the model endpoint and managed runtime share one region. The probe forces the Google Cloud backend before agent construction, supports object- and dictionary-shaped stream events, and fails closed if `review_required` is false.
- The no-tools ADK probe returned a Pydantic-validated **FactChange** for Scene 12: wardrobe, blue jacket to black jacket, with `review_required: true`.
- A managed Agent Runtime invocation independently returned that same schema-valid FactChange from `projects/136906134633/locations/us-central1/reasoningEngines/6541647233790509056`. Packaging pins `cloudpickle` and `pydantic` alongside the Google ADK dependencies. The production Change Packet agent itself is a later integration gate, not yet a hosted proof.

## Change Packet Agent proof — 2026-08-17

- The real Change Packet agent was first invoked locally through Google ADK with the actual bounded Scene 12 packet input. The initial invocation exposed a prompt ambiguity: it treated the deterministic `At risk` readiness label as a `review_required` packet status. The instruction was tightened and the probe now fails closed unless an actionable packet returns `ready`, cites only the supplied evidence IDs, recommends only Wardrobe and Assistant Director, and sets `distinguishes_unknowns` to `true`.
- The corrected agent passed locally, then was deployed to `projects/136906134633/locations/us-central1/reasoningEngines/4527341931704877056` using `gemini-2.5-flash` in `us-central1`.
- The deployed runtime independently returned `ready`, cited only `ev-dailies-11-blue`, `ev-call-sheet-13`, and `ev-call-sheet-14`, recommended exactly Wardrobe plus Assistant Director, and declared that it distinguishes supplied evidence from unknowns.
- This proves the actual explanatory Change Packet agent. Wiring that resource into the public FastAPI application remains a separate integration and hosting gate.

## Definition of done

The foundational external-service proof gates are complete: the reader query, writer event, denial checks, and deployed Google structured FactChange response are visibly real and documented without committing credentials. The next build gate is wiring the real ClickHouse path and then a deployed Change Packet agent into the public application.
