# Build Checklist

## Build Preferences

- **Build mode:** Autonomous. Codex owns sequencing and makes safe, scoped implementation decisions.
- **Comprehension checks:** N/A. Explanations are included only where a cloud, security, or product decision affects Ezra's choices.
- **Git:** Local milestone commits after verified foundations, functional MVP, and release candidate; no remote publication or public-repository change without Ezra's explicit go-ahead.
- **Verification:** Yes. Pause for the real Google + ClickHouse runtime proof and for the visible product-quality review; all other safe work proceeds autonomously.
- **Check-in cadence:** Speed-run, evidence-first. Report completed work, verification evidence, blockers, and any improvement made at each checkpoint.
- **Submission wow moment:** A Scene 12 revision triggers a visibly real ClickHouse evidence trace, then ends in a human-approved follow-up with a reader-verified shoot-readiness receipt.

## Checklist

- [ ] **1. Complete the real-runtime access gate**
  Spec ref: `spec.md > External APIs And Dependencies`, `spec.md > Risks And Verification`
  What to build: Create/select the isolated GCP project, attach the approved credit and budget alert, create the small ClickHouse Cloud service, and configure least-privilege reader/writer identities in Secret Manager. Keep every value out of Git and the browser.
  Acceptance: A deploy-capable identity can use Gemini in `us-central1`; distinct ClickHouse reader and writer credentials exist; the reader cannot write and the writer cannot run broad reads or drop data.
  Verify: Follow `docs/sprint-0-google-runbook.md` and `docs/sprint-0-clickhouse-runbook.md`; record non-secret PASS evidence in `docs/sprint-0.md`.

- [x] **2. Prove the partner and agent runtimes before product code**
  Spec ref: `spec.md > Stack`, `spec.md > External APIs And Dependencies`
  What to build: Run the existing pinned ClickHouse MCP reader/write/read proof and the schema-constrained Gemini ADK proof against real services; deploy and invoke the minimal Agent Runtime proof.
  Acceptance: One real reader query, one allowed writer event, reader verification, denied negative checks, and one deployed Agent Runtime structured response all succeed without credentials in source control.
  Verify: real ClickHouse reader/write/read and denial checks passed through the pinned MCP server; the deployed Agent Runtime returned the schema-valid Scene 12 Change Packet. Retain only redacted output and resource names in Sprint 0 notes.

- [ ] **3. Create the deployable application foundation**
  Spec ref: `spec.md > File Structure`, `spec.md > Architecture`
  What to build: Scaffold the React/TypeScript/Vite client and FastAPI application, production Docker build, health endpoint, typed settings, local `.env` loading, static-asset serving, and test runners. Retain the existing probes independently.
  Acceptance: A local app starts with no secrets committed, renders a deliberate loading/failed-configuration state, and `GET /healthz` has no sensitive detail.
  Verify: Run backend type/tests and frontend build; build the container image locally; inspect `git diff` and secret scan results.
  Current sequencing note: the Python foundation may progress while Marketplace approval is pending, but this item cannot be marked complete until the unavailable Node/Vite and container checks pass. The real ClickHouse and Google runtime proofs remain mandatory before any hosted-product claim.

- [ ] **4. Model and seed the six-scene production memory**
  Spec ref: `spec.md > Data Model`, `spec.md > Data Flow > C. Abstention and recovery`
  What to build: Add ClickHouse append-only schema, curated marts, self-authored six-scene seed data, and the 15–20 labeled mutation fixtures. Scope runtime events to a signed `demo_session_id`; reset mints a new fixture session and can never target/delete an arbitrary database.
  Acceptance: A clean seed produces Scene 12 blue jacket, Scene 11 already-shot evidence, and two upcoming dependent scenes with stable IDs; each expected/abstention fixture is documented; concurrent demo sessions cannot see or reset one another's events.
  Verify: Apply schema and seed against the real demo database; query only through the reader adapter; run fixture-consistency tests, two isolated-session resets, and a non-destructive-data check.

- [ ] **5. Build the safe ClickHouse MCP adapter boundary**
  Spec ref: `spec.md > Architecture > Trust and authority model`, `spec.md > Components And Responsibilities > ClickHouse MCP Adapters`
  What to build: Implement isolated reader/writer stdio MCP adapters, named query and insert templates, configuration redaction, correlation IDs, public trace-event construction, and fail-closed error handling.
  Acceptance: The backend can complete the required named reads/writes; the agent receives only read context; no route, model output, or user input can become SQL.
  Verify: Unit-test template selection and redaction; run reader/write permission-negative checks; review a trace log for secrets and raw connection details.

- [ ] **6. Build the deterministic revision and impact API**
  Spec ref: `spec.md > Data Flow > A. Apply the prepared revision`, `spec.md > API Contracts`
  What to build: Add Pydantic contracts, `GET /api/demo/state`, `POST /api/revisions`, revision persistence, curated-evidence lookup, deterministic continuity/schedule rules, impact snapshots, and missing/contradictory-evidence states.
  Acceptance: Blue jacket → black jacket produces exactly the Scene 11 continuity conflict and two scheduled dependencies with source IDs; unsupported values fail safely; no evidence withholds action.
  Verify: Run unit tests for every labeled fixture plus API tests for valid, invalid, missing, and contradictory cases; inspect real ClickHouse records through the reader path.

- [ ] **7. Integrate the bounded Google Change Packet agent**
  Spec ref: `spec.md > AI Usage`, `spec.md > Components And Responsibilities > Change Packet Agent`
  What to build: Implement the ADK input/output models, grounded instructions, Agent Runtime gateway, response validation, deterministic fallback copy, and agent-result trace step.
  Acceptance: The agent cites only supplied evidence IDs, preserves deterministic labels, distinguishes unknowns, and can recommend only the allowed Wardrobe + Assistant Director follow-up.
  Verify: Run schema/contract tests with invalid evidence IDs and labels; invoke the real deployed agent for the happy path and one abstention case.

- [ ] **8. Close the human action and readiness loop**
  Spec ref: `spec.md > Data Flow > B. Create the human-approved follow-up`, `spec.md > Components And Responsibilities > Follow-up and Decision Receipt Service`
  What to build: Add actionability checks, session-scoped `Idempotency-Key` handling, follow-up creation, readiness-event persistence, reader-confirmed Decision Receipt, and non-destructive demo-session reset state.
  Acceptance: Only a supported packet can create one follow-up; a matching repeat request returns the original action ID; a reused key with a different payload returns `409`; the receipt names owners and transitions `At risk` to `Follow-up created`.
  Verify: API/integration tests run the happy path twice, assert cross-session isolation, and inspect event count, IDs, owners, and reader-confirmed readiness.

- [ ] **9. Build the premium Continuity Command Desk**
  Spec ref: `spec.md > Components And Responsibilities > Command Desk Interface`, `prd.md > Epic 1`, `prd.md > Epic 2`
  What to build: Implement the focused Scene 12 start state, prepared revision control, responsive layout, accessible keyboard/focus behavior, loading/failure states, and the black/green ClickHouse-adjacent design system.
  Acceptance: A judge immediately sees the production context, current blue-jacket fact, and one dominant action without a generic dashboard, configuration screen, or chat surface.
  Verify: Run frontend tests and a desktop/mobile visual pass; manually complete the first interaction in a clean browser in under ten seconds.

- [ ] **10. Build the Change Packet, Live Evidence Trace, and receipt**
  Spec ref: `spec.md > Components And Responsibilities > Change Packet and Evidence Panel`, `prd.md > Epic 3`, `prd.md > Epic 4`, `prd.md > Epic 5`, `prd.md > Epic 6`
  What to build: Render the impact-summary strip, source-evidence cards, deterministic impacts, bounded explanation, stepwise yellow MCP/query trace, one compact Runtime proof expansion, single `Create follow-up` action, and the in-place calm decision receipt.
  Acceptance: Evidence appears before the action; green represents confirmed states, yellow only query/evidence moments; Runtime proof shows MCP version, sanitized correlation/action IDs, read/write/read states, and reader-confirmed readiness without raw SQL/endpoints/secrets; the receipt visibly proves owner, action ID, and readiness transition.
  Verify: Playwright runs the full happy path and captures screenshots; test no-evidence, failed-analysis, and duplicate-action render states; verify the Runtime proof fields against live trace events; complete the visual-quality review pause here.

- [ ] **11. Deploy, harden, and rehearse the public proof**
  Spec ref: `spec.md > Risks And Verification`, `spec.md > Definition of done`
  What to build: Deploy Cloud Run and Agent Runtime, inject secrets through Secret Manager, configure minimum IAM, add redacted Cloud Logging, publish reset/setup runbooks, and run clean-browser reliability rehearsals.
  Acceptance: The public URL completes three consecutive clean runs; logs and source scan show no secrets; the hosted app visibly uses real ClickHouse and Google paths.
  Verify: Cloud Run smoke test, deployed end-to-end Playwright test, three manual clean-browser runs, dependency audit, secret scan, and production-log review.

- [ ] **12. Prepare Devpost handoff**
  Spec ref: `prd.md > Submission Proof Points`, `spec.md > Demo And Submission Flow`
  What to build: Gather the project story, architecture/proof map, public repository with OSI license, screenshots, three-minute functional demo recording, reset instructions, and final Devpost copy.
  Acceptance: The participant has enough material to run `$prepare-submission`, and the first 30 seconds unmistakably show revision → ClickHouse trace → evidence → verified readiness receipt.
  Verify: Run the full demo script from a clean browser, review the video against the proof map, check all submission assets, and confirm the next command is `$prepare-submission`.
