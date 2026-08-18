# Product Requirements Document

## Product Summary

SlateGuard is a production change-intelligence application for a script supervisor. It turns a typed revision into a compact, evidence-backed Change Packet: what changed, which production records it affects, why the impact matters, who must follow up, and what the resulting shoot-readiness state is.

The hackathon release must make one complete change-control loop feel real and satisfying. It must not behave like a generic chatbot, a broad studio dashboard, or a passive continuity checklist.

## Target User

**Primary user:** a script supervisor responsible for noticing and documenting continuity implications of creative revisions.

**Moment of use:** immediately after a revision to a known production fact, before the change reaches an already-shot scene or an upcoming call sheet.

**User outcome:** in under a minute, the supervisor knows whether the change creates a real production issue, sees the source evidence, creates the right follow-up, and leaves behind a durable decision record.

## Product Principles

- **Evidence before confidence.** Every impact claim must visibly point to a source record.
- **Human decision, not autonomous action.** SlateGuard can explain and recommend; the user owns the consequential follow-up.
- **One clear story.** The primary path is a single revision, not a collection of loosely related tools.
- **Technical proof as product.** The Live Evidence Trace is a legible product element, not hidden developer logging.
- **Calm authority.** The interface is query/evidence-forward and ClickHouse-adjacent, using near-black, decisive green, and constrained yellow query signals.

## Core User Journey

1. The supervisor arrives at a focused demo-production view with Scene 12 selected.
2. They see the current wardrobe fact: **blue jacket**. A single primary action applies the prepared revision to **black jacket**.
3. The app transitions to the Change Packet and visibly progresses through the Live Evidence Trace.
4. The packet presents the old/new fact, three source evidence records, and two explicit impacts:
   - Scene 11 has already been filmed with the blue jacket.
   - Two dependent scenes scheduled for the next shoot still use the blue-jacket fact.
5. The user reads a concise grounded explanation and sees a single recommended action: create a Wardrobe + Assistant Director follow-up.
6. The user selects `Create follow-up`.
7. The packet ends on a calm decision receipt: follow-up created, owners, action identifier, and readiness transition. The user never has to infer whether the outcome persisted.

## Epics And User Stories

### Epic 1: Start from a believable production record

- As a script supervisor, I want to start inside a credible demo production so that I can understand the context of the revision without setting up data.

Acceptance criteria:

- The first screen identifies the production, Scene 12, and the current wardrobe value.
- The screen has one dominant `Apply revision` action and no required login, upload, or configuration step.
- A quiet secondary link may open the Scene Ledger, but the primary demo path does not require it.
- The visual hierarchy signals that the user is about to change one specific, consequential production fact.

### Epic 2: Apply one clear creative revision

- As a script supervisor, I want to apply a constrained scene-fact change so that I can see whether it creates downstream risk.

Acceptance criteria:

- Selecting `Apply revision` changes the displayed wardrobe fact from blue jacket to black jacket.
- The user can see the previous value, proposed value, scene number, and revision status.
- The app does not expose arbitrary database or agent instructions to the user.
- The user receives immediate visual confirmation that analysis has begun.

### Epic 3: Inspect a grounded Change Packet

- As a script supervisor, I want an evidence-backed explanation of a revision's blast radius so that I can make an informed follow-up decision.

Acceptance criteria:

- The Change Packet clearly distinguishes the revision from the resulting impacts.
- It displays the three primary source records: Scene 11 dailies, a current production-fact record, and affected upcoming call-sheet/dependency records.
- It names the two impact types in plain language: continuity conflict and downstream schedule dependency.
- It identifies the affected scenes and whether each is already shot or scheduled.
- It gives a concise, non-speculative explanation of why the change matters.
- The primary evidence is visible without requiring the user to inspect a separate dashboard.

### Epic 4: Make the data path visible

- As a judge or technical reviewer, I want to see that the result came from real production data and a real action path so that I can trust the demonstration.

Acceptance criteria:

- A compact Live Evidence Trace shows a readable sequence: revision saved, evidence retrieved, rule triggered, follow-up saved, readiness refreshed.
- Each trace step has a distinct status: in progress, complete, or needs review.
- Query/evidence moments use the constrained ClickHouse-yellow accent; green is reserved for confirmed product states.
- The trace supplements the Change Packet rather than competing with it for attention.

### Epic 5: Keep consequential action human-owned

- As a script supervisor, I want to create a clear follow-up from the evidence packet so that Wardrobe and the Assistant Director know what requires review.

Acceptance criteria:

- The Change Packet exposes one primary action: `Create follow-up`.
- The follow-up is pre-addressed to Wardrobe and the Assistant Director; there is no assignment-management interface.
- The action is available only after the app has presented a supported evidence-backed impact.
- Selecting the action produces a visible durable result, not merely a toast message.

### Epic 6: Close the loop with readiness and decision memory

- As a script supervisor, I want a persisted decision receipt and readiness state so that the issue is not rediscovered or silently lost.

Acceptance criteria:

- The post-action receipt states the follow-up state, owners, timestamp/action identifier, and readiness transition.
- The readiness state clearly distinguishes `At risk`, `Follow-up created`, and `Review required`.
- The user can see that the decision is associated with the same Scene 12 revision and source evidence.
- Re-running the clean demo begins from a known baseline, not from a partially completed prior session.

## Edge Cases

### No supporting evidence

If the selected revision has no relevant source evidence, SlateGuard must show `Review required`, explain that it cannot verify a production impact, and withhold the follow-up action. It must never invent an evidence-backed conflict.

### Contradictory evidence

If production records disagree, the packet must show the contradiction as `Review required`, retain both relevant source records, and avoid a definite recommendation.

### Failed or incomplete analysis

If analysis cannot complete, the user sees a stable recovery state explaining that no decision was recorded. The prior production state remains visible and the user may retry the known demo path.

### Repeat action

If the follow-up already exists for the same revision, SlateGuard shows the existing action receipt and does not create a duplicate follow-up.

### Return visit

If a reviewer returns after completing the core path, the demo can be reset to the known baseline. The decision receipt and readiness transition remain available during the active session so the result is inspectable.

## What We Are Building

- One prepared Scene 12 wardrobe revision: blue jacket → black jacket.
- One polished Change Packet screen with evidence, impact, explanation, trace, and action.
- One human-owned `Create follow-up` action and decision receipt.
- One readiness transition, with supported `Review required` / missing-evidence states.
- One Scene Ledger as a secondary evidence view.
- A premium, calm, ClickHouse-adjacent visual system with Kalshi-like black-and-green color confidence.

## What We Would Add With More Time

- Additional revision types such as props, locations, time-of-day, and dialogue.
- Multiple open Change Packets and a true production-level readiness overview.
- Department assignment controls, comments, reminders, and collaboration.
- Uploads, real script parsing, video/dailies analysis, and integrations with production software.
- Authentication, role permissions, and multi-production support.

These are deliberately deferred because they dilute the proof of the required core loop.

## Submission Proof Points

- A public app visibly completes the revision → evidence → human action → readiness loop.
- A real ClickHouse-backed evidence trace is visible during that loop.
- The user sees source records and deterministic impact labels before the action.
- Google-powered agent explanation is grounded in the displayed evidence.
- The public repository maps the visible trace to the actual runtime path and contains setup/reset instructions.
- The three-minute demo can reproduce the core journey from a clean baseline without manual repair.
