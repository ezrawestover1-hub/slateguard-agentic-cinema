# SlateGuard — Evidence-First Production Change Control

## One-line Summary

SlateGuard turns a creative production revision into a ClickHouse-backed evidence packet, a human-owned follow-up, and a verified shoot-readiness update.

## Problem

Film and television changes rarely stay isolated. A seemingly simple request—change Scene 12's wardrobe from a blue jacket to a black jacket—can conflict with completed dailies, affect upcoming call sheets, and require action from several departments. Today's scripts, messages, and spreadsheets make it hard for a script supervisor to see the evidence, understand downstream impact, and leave a durable record of the decision.

## Solution

SlateGuard is a Continuity Command Desk for a single high-stakes revision loop. Before the agent explains an impact, its Impact Pulse narrows the ClickHouse context to Scene 11 history, the Scene 12 revision, and the next scheduled dependencies. A script supervisor applies the revision, then SlateGuard writes the change through a constrained ClickHouse writer MCP path, retrieves curated production evidence through a separate reader MCP path, and presents a grounded Change Packet. The operator can create a follow-up only after seeing the evidence; the product then persists and reader-verifies the resulting readiness transition.

The demo uses six self-authored fictional production scenes. Its core workflow changes Scene 12 from a blue jacket to a black jacket, surfaces Scene 11 dailies and scheduled dependencies, assigns Wardrobe and the Assistant Director, and ends with a traceable decision receipt.

## Why This Matters

SlateGuard turns an ambiguous creative request into an accountable operational decision. It keeps a human in charge of the consequential action while making the relevant source evidence and system trace visible first. That pattern can help productions catch continuity and scheduling risk before it becomes a costly shoot-day surprise.

## How We Used AI

SlateGuard uses a schema-constrained Gemini Change Packet agent on Google Cloud to turn bounded, retrieved production facts into a readable impact explanation. The agent receives curated evidence and deterministic findings—not arbitrary database access—and its output is validated against the allowed evidence IDs and owners. If evidence is missing, contradictory, unsupported, or the model is unavailable, the workflow fails closed to an explicit review state rather than inventing a conclusion.

## How We Used Codex

Codex was used as an engineering partner to scope the narrow judge-visible workflow, turn it into a PRD and technical specification, implement the React/TypeScript command desk and FastAPI service, create the least-privilege ClickHouse MCP boundary, build test coverage, and diagnose deployment issues. It also iterated the ClickHouse-adjacent visual system, prepared the Cloud Run container and Cloud Build test gate, and verified the hosted evidence loop without exposing credentials or raw production endpoints.

## Key Features

- **Evidence-first change control:** the interface makes the creative revision, source evidence, impact assessment, and human action legible in that order.
- **Live ClickHouse relevance pulse:** fixed reader-MCP aggregates surface only the active production window; archive, unrelated, and unscheduled work is excluded by policy before the agent acts.
- **Separated ClickHouse MCP identities:** a reader can query only curated views; a writer can append approved event records but cannot read production data or drop data.
- **Grounded Change Packet:** Gemini explains only the bounded evidence it is given and distinguishes a verified result from a review-required state.
- **Human-owned follow-up:** SlateGuard does not autonomously create a consequential production task; an operator decides after reviewing the evidence.
- **Verified readiness receipt:** the follow-up and readiness transition are written, then checked back through the reader path before the receipt is shown.
- **Safe public-demo sessions:** short-lived, session-scoped event history and idempotency controls prevent one demonstration from overwriting another.

## Architecture

```text
React / TypeScript Command Desk
        |
        v
FastAPI service on Cloud Run
        |------------------------------|
        v                              v
Gemini Change Packet agent       Official mcp-clickhouse sidecars
(structured, bounded facts)      reader: curated views only
                                  writer: append-only event templates
                                           |
                                           v
                                  ClickHouse Cloud production memory
```

The browser never receives database credentials or arbitrary SQL capability. Deterministic backend rules own typed writes and impact decisions; the reader MCP path supplies evidence; the agent explains supplied facts; and the operator alone creates the follow-up.

## Testing Instructions

1. Open the public demo URL below in a fresh browser session.
2. Confirm the Command Desk shows the Scene 12 blue-jacket to black-jacket revision and a verified runtime status.
3. Select **Apply revision**. The trace should show writer persistence, reader evidence retrieval, and Change Packet validation.
4. Inspect the cited dailies and schedule evidence, including the affected owners.
5. Select **Create follow-up** and confirm the decision receipt names the owners and the reader-verified readiness transition.
6. For automated validation, Cloud Build runs the backend unit suite before an image is deployed; the current build gate covers 40 backend tests across API, MCP boundary, flow, and agent-contract behavior.

## Public Demo Link

https://sprint2---slateguard-vseh3ye7mq-uc.a.run.app

The live demo is currently deployed on Google Cloud Run. Its public Sprint 2 build has been browser-verified through writer persistence, reader retrieval, grounded Change Packet validation, and the live ClickHouse Impact Pulse. It uses self-authored fictional production data only.

## Public Repository Link

**TODO — repository is not public yet.** The project contains an MIT license, but a public repository URL must be created and added here before the final Devpost form is completed. Before publishing, scan for `.env` files, API keys, tokens, and deployment credentials.

## Demo Video

**TODO — upload the final public video link.** The submission asset is rendered and validated locally at `slateguard-demo-video/out/slateguard-proof-cut.mp4`: 180 seconds, 1920×1080, H.264, caption-led, with the deployed Impact Pulse and reader-verified receipt. The strongest final upload will intercut it with one uninterrupted live browser recording using the matching narration in `slateguard-demo-video/NARRATION.md`.

### Recommended 3-minute cut

| Time | What the judge sees | Proof point |
| --- | --- | --- |
| 0:00–0:15 | The blue-to-black Scene 12 revision and why it can affect a shoot | Clear production problem |
| 0:15–0:45 | Apply the revision in the Command Desk | The core operator action |
| 0:45–1:15 | Writer → reader → Change Packet trace resolves | ClickHouse is active in the core loop |
| 1:15–1:45 | Cited Scene 11 dailies and downstream schedule evidence | Grounded evidence, not a generic chat answer |
| 1:45–2:15 | Create the human-owned follow-up and show the verified receipt | Durable human decision and readiness update |
| 2:15–2:45 | Show the architecture / trust boundary | Separate reader-writer MCP roles and safe AI boundary |
| 2:45–3:00 | Restate the benefit: evidence before action | A reusable operational-control pattern |

## Screenshot Shot List

1. **Command Desk overview** — Scene 12 revision visible before action, premium black/green product shell, and verified runtime status.
2. **Live evidence trace** — the three resolved stages: writer persistence, reader retrieval, and grounded Change Packet validation.
3. **Source evidence panel** — Scene 11 dailies plus scheduled dependencies with evidence IDs and affected owners.
4. **Decision receipt** — Wardrobe and Assistant Director follow-up plus reader-verified readiness update.
5. **Trust-boundary / architecture frame** — concise view of Gemini, Cloud Run, official ClickHouse MCP reader/writer sidecars, and ClickHouse Cloud.
6. **Impact Pulse** — the active-scene scope and live reader-MCP aggregate counts, shown before the revision action.

Final live-browser captures, all using the self-authored fictional demo data:

- `docs/demo-captures/01-command-desk-before.png` — the initial revision, cited evidence, owners, and protected path before action.
- `docs/demo-captures/02-revision-trace-confirmed.png` — writer persistence, reader retrieval, and grounded Change Packet validation.
- `docs/demo-captures/03-followup-receipt-verified.png` — reader-verified action receipt and `At risk → Follow-up created` readiness transition.
- `docs/demo-captures/04-impact-pulse-preview.png` — local release-candidate visual check of the active-scope pulse.
- `docs/demo-captures/05-impact-pulse-deployed.jpg` — deployed Cloud Run capture showing the live reader-MCP production window and the confirmed revision trace.
- `docs/demo-captures/06-deployed-decision-receipt.jpg` — deployed Cloud Run capture showing the human-owned follow-up and reader-verified `At risk → Follow-up created` receipt.

Earlier local design references remain available for comparison only:

- `frontend/design-reference/command-desk-local-v1.png`
- `frontend/design-reference/command-desk-mobile-v1.png`
- `frontend/design-reference/command-desk-concept-v1.png`

## Submission Readiness Notes

### Working now

- Public Command Desk deployed to Cloud Run.
- The live revision flow has shown writer persistence, reader evidence retrieval, and Change Packet validation.
- A prior end-to-end follow-up was persisted and reader-verified, producing a durable receipt for the Scene 12 flow.
- The live Impact Pulse is deployed and browser-verified: its reader-MCP aggregates surface the active production window before the revision action.
- The complete public fictional workflow is now browser-verified: revision persistence, reader retrieval, grounded packet validation, human-owned follow-up, and reader-verified readiness receipt.
- Cloud Build enforces the backend test suite before deployment.
- The project has a judge-facing README, technical runbooks, an MIT license, and a timed demo script.

### Must finish before final Devpost action

- Publish a sanitized public repository and add its URL.
- Capture 3–5 final live screenshots, including the receipt state.
- Upload the rendered functional three-minute video (optionally intercut with one uninterrupted live-browser recording); add its public URL.
- Rehearse the public demo from a clean browser and capture the latest receipt state on video.
- Verify the exact Devpost form fields and any sponsor-track requirements against the live event form.

## Known Limitations

- This hackathon slice intentionally supports one prepared production scenario, not a full production-management suite.
- The fictional production memory is self-authored for the demo; no real production data is included.
- Follow-up assignment is represented as a durable in-product event; external project-management notifications are out of scope.
- The public repository and recorded video are not available yet.

## TODO Official Form Fields

The authenticated Devpost event is open and the participant is registered. The live requirements lookup was unavailable during drafting because the connector rejected the expected event parameter schema, so the following are intentionally **not** guessed:

- [ ] Exact event-specific project-form fields and character limits
- [ ] Official sponsor/category selection and any ClickHouse-specific eligibility language
- [ ] Final public repository URL
- [ ] Final demo-video URL
- [ ] Final screenshot uploads
- [ ] Any required team-member, AI disclosure, or Codex session-ID field
