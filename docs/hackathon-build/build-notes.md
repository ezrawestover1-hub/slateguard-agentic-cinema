# Build Notes

## Onboarding — 2026-08-14

- The participant chose the optional guided build path after completing the Devpost registration, rules, and resources stages.
- Existing planning artifacts establish SlateGuard as the working project: a ClickHouse-track production change-control agent with one narrow, evidence-first revision loop.
- Sprint 0 has a tested local Google ADK and official ClickHouse MCP scaffold; real cloud/runtime proof remains pending participant-owned GCP and ClickHouse provisioning.
- Interview round 1 is pending: participant coding background and any preferred refinements to the initial idea.

## Onboarding interview — round 1

- The participant uses Codex and the terminal.
- The participant requests continuous improvement discipline: make safe positive changes proactively, flag material decisions, and state when a higher-reasoning model would add meaningful value.

## Onboarding interview — round 2

- The participant delegated product decisions to Codex.
- Chosen primary operator: script supervisor.
- Chosen demo: Scene 12 wardrobe revision, blue jacket → black jacket.
- Chosen first 30-second proof: the live evidence trace, followed by the Change Packet and human follow-up/readiness update.
- Chosen provisioning preference: browser-guided flow; explicit confirmation remains required before billed-resource or billing changes. A GCP account is available; no account credentials or email address are stored in project files.

## Onboarding interview — round 3

- Chosen interface direction: Continuity Command Desk. The design should center a single Change Packet, visible source evidence, a compact live MCP evidence trace, and a deliberate human decision action rather than generic chat or dashboard surfaces.
- Initial visual direction was premium, calm, authoritative, grounded; warm creams and restrained greens.
- Participant correction: the design must be highly compatible with the ClickHouse-adjacent track. Final direction is black/charcoal, off-white, and ClickHouse yellow; green is reserved for semantic readiness confirmation.
- Final visual refinement: adopt a high-signal Kalshi-like green as the primary product/action color on a near-black shell. ClickHouse yellow remains a constrained technical accent for the MCP query/evidence trace; off-white appears only in source-excerpt surfaces.
- Participant clarification: ClickHouse—not Kalshi—is the product-reference layer. Borrow Kalshi only for color treatment; make the workflow, data density, evidence trace, and technical feel ClickHouse-adjacent.

## Scope interview

- Time budget: 120+ focused hours before the Sept. 5 feature freeze.
- Scope decision: do not broaden product surface area because time is available; use the extra capacity for live-runtime reliability, fixture evaluation, deployment, visual refinement, and recording rehearsal.

## Scope interview correction

- Superseded time estimate: the participant confirmed 120+ focused hours before the Sept. 5 feature freeze. Retain a roughly 70-hour core scope and reserve the additional capacity for proof reliability and polish, not feature expansion.
- Delivery calibration: participant reports shipping Westover EPR in one week. The referenced public site could not be inspected from this environment, so no unverified design assumptions were taken from it.

## Scope decision

- The participant's product-development context supports a top-three-oriented thin slice: explicit contracts, durable state, acceptance criteria, and evidence over claims.
- The scope is locked around a single script-supervisor revision workflow. Extra time is committed to runtime proof, fixtures, deployment, visual refinement, and video rehearsal rather than product breadth.
- `scope.md` created with the ClickHouse-adjacent interaction model and Kalshi-color-only visual rule.

## PRD interview

- Chosen experience sequencing: keep the pre-change screen focused on the revision; reveal detailed source evidence only after the change triggers the impact workflow. A quiet secondary Scene Ledger link may exist, but it is not part of the demo path.
- Chosen completion state: after `Create follow-up`, show a calm decision receipt with the persisted action ID, owners, and readiness transition in place. Do not redirect to a separate dashboard before the judge sees the durable result.

## PRD decision

- `prd.md` created. It defines six user-facing epics, testable acceptance criteria, evidence/decision sequencing, and five edge states.
- The PRD preserves the narrow scope: one prepared revision, one human action, and one durable result. Technical implementation choices remain for the next specification step.

## Technical specification decision

- `spec.md` created. The build is a React/TypeScript command desk and FastAPI BFF on Cloud Run, one schema-constrained Google ADK Change Packet agent on Agent Runtime, and one real ClickHouse Cloud service reached only through the official `mcp-clickhouse` package.
- The system boundary is explicit: deterministic backend code owns typed writes and impact decisions; the reader MCP path supplies curated evidence; the agent only explains supplied facts; a human alone can create the consequential follow-up.
- The deployment risk is intentionally first-class: real reader/write/read and Agent Runtime proofs must pass before UI work expands.

## Checklist decision

- The participant approved the recommended hand-off: Codex owns checklist sequencing and runs autonomously.
- Verification pauses are limited to the real Google + ClickHouse runtime proof and the visible product-quality review. All safe, scoped work between them proceeds without routine permission prompts.
- Submission wow moment is locked: the Scene 12 revision visibly flows through the ClickHouse evidence trace and ends with a human-approved, reader-verified readiness receipt.
- `checklist.md` contains twelve ordered milestones. It deliberately puts managed-runtime proof before product-code investment and reserves the final phase for public-host reliability, recording, and Devpost handoff.

## Build started — access-gate preflight

- Build mode is now active. The first unchecked checklist item is the required real-runtime access gate; it is intentionally ahead of frontend or product scaffolding so the ClickHouse integration cannot become decorative.
- Safe preflight confirmed that `gcloud` is not installed and no local `.env` is present. No cloud account, billing setting, ClickHouse service, credential, or external resource was modified.
- Added `docs/runbooks/access-gate.md` with the minimum approved resource shape, a $300 budget-alert strategy, least-privilege identity plan, and a secret-safe handoff format.

## Build checkpoint — GCP project and budget

- Created the isolated GCP project `slateguard-agentic-cinema-2026`, confirmed its billing linkage to the existing credit-backed billing account, and created a $300 monthly budget alert.
- The Google Cloud Console API-library page then failed to load before API enablement. Following the autonomous-build recovery rule, no retry loop or alternative provisioning path was attempted in the same checkpoint.
- Proposed recovery: use the signed-in Google Cloud Shell only to run an explicit allowlist of required `gcloud services enable` commands, then return to the browser for visible verification. This is a controlled equivalent of the failed console action, not an architecture or scope change.

## Build checkpoint — Cloud Shell access state

- The participant approved the Cloud Shell fallback and its Google credential authorization prompt was accepted.
- The intended allowlisted `gcloud services enable` command did not change project state: Cloud Shell reported that no active `gcloud` account is selected and stopped before enablement. No API was partially enabled.
- The next required external-state action is an interactive `gcloud auth login` in Cloud Shell. After it succeeds, repeat the same fixed allowlist command once and verify enabled services before moving to ClickHouse.

## Build checkpoint — required GCP APIs enabled

- After the participant completed the one-time Cloud Shell OAuth flow, the explicit `gcloud services enable` allowlist completed successfully in `slateguard-agentic-cinema-2026`.
- Enabled services: Vertex AI, Cloud Run, Artifact Registry, Secret Manager, Cloud Storage, Cloud Logging, Cloud Monitoring, Cloud Resource Manager, Service Usage, Telemetry, and Cloud Trace.
- This resolves the Google-side access prerequisite without creating a deployable runtime, agent, secret, or data service. The next hard dependency is the real ClickHouse Cloud service and its separate reader/writer identities.

## Build checkpoint — ClickHouse account access blocked

- The ClickHouse Cloud console was reached and the participant-approved Google sign-in consent was completed, but ClickHouse returned a session/cookie failure instead of an authenticated console.
- No retry loop was attempted. No ClickHouse organization, service, database, password, or spend was created.
- Recovery proposal: establish one clean ClickHouse Cloud session in the browser, then resume the existing access-gate checklist at service creation. The GCP project, billing guardrail, and required API proof are already complete and remain intact.

## Parallel readiness audit — 2026-08-15

- Three independent tracks reviewed ClickHouse recovery, implementation readiness, and top-three proof quality while the ClickHouse access gate is blocked.
- Safe corrective change: the ClickHouse writer-read negative check now queries the smoke table rather than a constant, so it actually proves the writer lacks project-table `SELECT` permission. Its child environment now begins from a minimal allowlist instead of inheriting the parent process environment.
- Architecture improvement: public demo reset will mint a signed, short-lived `demo_session_id` and scope all append-only runtime events to it. This prevents destructive shared-data resets and makes concurrent judge sessions safe.
- Proof improvement: the Change Packet gains a compact Runtime proof expansion (MCP version, redacted correlation/action IDs, read/write/read state, and reader-confirmed readiness), plus a production-impact summary strip and an explicit abstention proof in submission materials.

## Build checkpoint — Marketplace activation pending

- The Google Cloud Marketplace page explicitly reports that the ClickHouse Cloud subscription is pending ClickHouse approval.
- The Marketplace signup handoff was exercised once and did not yet open a ClickHouse service console; it returned to the pending subscription state.
- No service, database, credential, or billable ClickHouse workload is verified. The access gate remains open only for the external approval signal; no retry loop is warranted.

## Controlled parallel foundation — 2026-08-15

- Marketplace approval is externally pending and the local environment has no Docker-compatible ClickHouse runtime or Node/Vite toolchain. Rather than imply the partner proof is complete, the build now permits a narrowly scoped Python application foundation in parallel.
- This does not complete checklist item 3 or reorder the required runtime proof. Frontend, container, ClickHouse MCP, Agent Runtime, and deployment verification remain blocked until their actual environments are available.

## Controlled parallel domain core — 2026-08-15

- Added typed revision/evidence/dependency contracts and pure deterministic rules for the single supported Scene 12 wardrobe revision.
- The happy path yields only the required continuity conflict and schedule dependency; missing or contradictory dailies records fail closed to `Review required` and cannot offer a follow-up.
- These rules do not query or imitate ClickHouse. Their input remains bounded curated evidence that will be retrieved through the real reader MCP path.

## Controlled parallel production memory — 2026-08-15

- Added append-only ClickHouse schema definitions, narrow reader views, and a self-authored six-scene fictional production seed. The dataset includes the exact Scene 11 dailies and Scene 13/14 scheduled dependencies needed for the visible happy path.
- Added an evaluation-fixture manifest covering the happy path, missing evidence, contradictory evidence, and an unsupported revision. Nothing has been applied to ClickHouse yet; actual schema/seed application remains a reader-verified runtime gate.

## Controlled parallel MCP boundary — 2026-08-15

- Added a server-only ClickHouse boundary with fixed reader/writer templates. The browser and future agent receive no SQL capability; scene IDs are allowlisted and UUID values are generated server-side.
- The unit seam validates curated-view reads, fixed revision writes, injection rejection, and public error redaction. The pending live step is wiring this seam to the official `mcp-clickhouse` stdio process and running it against ClickHouse Cloud.

## Controlled parallel demo safety — 2026-08-15

- Added signed, short-lived demo sessions plus session-scoped idempotency behavior. Reset will mint a fresh session rather than delete shared event history.
- The current in-memory ledger is a tested development seam only. The real public flow will store matching idempotency/event records through the writer MCP path and read them back through the reader path.

## Controlled parallel Change Packet contract — 2026-08-15

- Added a strict Gemini-facing input/output contract. The model receives bounded facts/findings and can cite only supplied evidence IDs or recommend only Wardrobe + Assistant Director.
- Invalid agent output and unavailable-model states fall back to factual deterministic packet copy. This preserves the product's evidence boundary before the real Agent Runtime gateway is connected.

## Controlled parallel revision flow — 2026-08-15

- Added the revision orchestration seam: session-scoped idempotency, revision write, curated evidence/dependency reads, deterministic rules, bounded agent validation, and factual fallback are one transaction-shaped flow.
- Test doubles prove the flow's ordering and its no-duplicate-write behavior; only the pending ClickHouse MCP and Agent Runtime adapters remain to make this a real hosted transaction.

## Controlled parallel API boundary — 2026-08-15

- Added reset and revision routes with an HTTP-only demo-session cookie and required `Idempotency-Key`. The routes fail closed when real services have not been injected.
- API tests exercise reset → revision → duplicate revision using isolated test doubles. This is an application contract proof, not a claim that the live ClickHouse or Agent Runtime path has run.

## Controlled parallel Google gateway — 2026-08-15

- Added the ADK Change Packet gateway with Gemini 3.5 Flash and a strict response schema. It sends only serialized bounded packet input, consumes only a final structured response, and exposes a non-diagnostic failure for deterministic fallback.
- Its contract is covered with fake streamed events. The actual Vertex initialization and deployed Agent Runtime invocation remain mandatory Sprint 0 checks.

## Controlled parallel follow-up flow — 2026-08-15

- Added the human-owned follow-up flow: it permits an action only from a stored actionable impact, writes the follow-up and readiness events, then requires reader verification before returning a receipt.
- The resulting receipt intentionally ends at `Follow-up created`; it never infers that a department has resolved the underlying continuity risk.

## Controlled parallel follow-up API — 2026-08-15

- Added the session-protected follow-up route. Its response is a typed receipt only after the follow-up/readiness write sequence and reader verification complete.
- API coverage now proves the full reset → revision → human follow-up HTTP contract with test doubles; live persistence remains a pending ClickHouse proof.

## Controlled parallel deployment artifact — 2026-08-15

- Added a multi-stage Cloud Run container definition and a minimal Cloud Run service manifest. The image compiles the React interface and serves it from FastAPI, while the manifest contains only non-secret deployment configuration.
- The deployment guide explicitly prohibits a public fixture/test-double release. The image must stay fail-closed until official ClickHouse and Agent Runtime proofs are attached through Secret Manager/IAM.

## Controlled parallel public-proof package — 2026-08-15

- Added a judge-facing README with the exact proof map, trust boundary, architecture, local commands, and runtime verification gates. It distinguishes built/tested contracts from pending live-service proof.
- Added an MIT license. No public repository or remote publication has been created yet.

## Controlled parallel demo rehearsal — 2026-08-15

- Added a timed three-minute functional demo script. Its first 30 seconds make the revision/evidence loop unmistakable, and it reserves visible time for the official MCP runtime proof, human-owned decision, reader-verified receipt, and a short abstention demonstration.
