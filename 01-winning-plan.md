# Agentic Cinema: highest-winnability solo plan

## Decision

Build **SlateGuard**, a tightly scoped production change-impact agent, for the **ClickHouse** track.

SlateGuard is for assistant directors and script supervisors. A producer applies a script or call-sheet revision; the agent compares the new version with a small production record, flags the specific downstream continuity impact, cites the evidence, and prepares a human-approved follow-up.

The core claim is deliberately narrow: *turn one production change into a clear, evidence-backed impact packet before it causes rework.* It is not an AI filmmaker, screenwriter, generic chatbot, or studio-management platform.

## Solo-builder scope rule

This plan assumes one builder. A working, elegant thin slice has a better chance than a multi-agent architecture that is only partly real. Build **one agent, one user, one revision workflow, one demo dataset, and one irreversible-seeming decision**.

Keep only these capabilities:

- Seed a six-scene fictional production with scripts, call-sheet rows, and dailies notes.
- Apply one revision: change a wardrobe, prop, time-of-day, or location fact.
- Detect two deterministic impact types: a continuity conflict and an already-shot/scheduled downstream dependency.
- Show source evidence, a short Gemini explanation, and one human action: `Create follow-up`.
- Persist the finding and decision in ClickHouse.

Cut all uploads, raw-video analysis, authentication, user management, calendars, chat, notifications, autonomous changes, multiple teams, and multiple partner integrations. A simple "Load demo → apply revision → review impact → create follow-up" path is the entire product.

## Non-negotiable event constraints

- The official rules state a hard submission deadline of **2:00 PM PT on 2026-09-07**. A separate date feed previously returned a later date; treat the earlier rules deadline as controlling. Freeze features no later than 2026-09-05.
- Build a functional media-and-entertainment agent with Gemini and Google Cloud Agent Builder plus a Partner Entity product or MCP.
- Select exactly one partner track. This plan targets ClickHouse.
- Publish a hosted project, a public open-source repository, and a complete detectable OSI license.
- Show real runtime use of Google Cloud and the selected partner in code. Naming them in a README is insufficient. For ClickHouse, this means the official **`mcp-clickhouse`** MCP server connected to a ClickHouse Cloud or self-hosted cluster.
- Use only Google Cloud AI tools and any built-in AI features of the chosen Partner product. The rules prohibit other AI models, agent frameworks, and AI APIs.
- Include a publicly viewable English or English-subtitled demo video of at most three minutes that shows the project actually working.
- A team can have at most four people.

## What needs to win

The official rules score four areas on a five-point scale, weighted equally. The targets below are internal planning targets, not official scores.

| Area | What Continuity OS must prove |
| --- | --- |
| Technological implementation | Gemini extracts/normalizes a small set of scene facts; ClickHouse stores and queries versions, dependencies, and decisions; deterministic checks identify conflicts; the app records evidence and one follow-up action. |
| Design | A script supervisor can see one revision, its affected work, source evidence, and a single explicit follow-up decision in one coherent workflow. |
| Potential impact | The pitch quantifies fewer manual review passes and earlier detection of conflicts that could otherwise cause rework. Demonstrate this with a small, labeled test set rather than an unsupported savings claim. |
| Quality of idea | The project solves a real production handoff problem using an agent plus data system—not merely a generative creative feature. |

## Why this has the best statistical edge

Current official data exposes the five tracks but not entrant counts, so no claim that ClickHouse is the least crowded is justified. The statistical strategy is instead to maximize the probability of a top-three entry:

`P(prize) = P(polished, working submission) × P(top 3 | polished submission)`

SlateGuard improves both terms:

- **High shipping probability:** one revision workflow, a seeded believable dataset, two deterministic checks, and a three-screen user interface.
- **High differentiation:** it is production change control, not an AI scriptwriter, idea generator, or bare chatbot.
- **Deep track fit:** ClickHouse holds the scene, asset, schedule, and conflict-event data used by the core loop. Removing it materially harms the product.
- **Low judge cognitive load:** an uploaded/revised scene creates an obvious, visual conflict with evidence and a recommended action.
- **Credible enterprise posture:** evidence, user permissions, audit history, and a human approval gate make it feel useful beyond a hackathon.

## Directional concept ranking

Scores below are a decision aid, not official scoring or evidence of track crowding. The composite weights official-rubric potential (60%), partner indispensability (15%), differentiation (15%), and shipping confidence (10%).

| Rank | Concept / track | Composite | Main tradeoff |
| --- | --- | ---: | --- |
| 1 | SlateGuard / ClickHouse | 4.5 / 5 | Needs carefully designed sample data and two rigorous rules. |
| 2 | RightsRoom / IBM | 4.1 / 5 | Strong impact, but rights-policy accuracy and source data raise implementation risk. |
| 3 | Dailies SRE / Grafana | 4.0 / 5 | Clear technical demo, but less directly cinematic and may look like an observability dashboard. |
| 4 | Access Director / IBM | 3.9 / 5 | Meaningful impact, but quality assessment of generated accessibility content is harder to prove. |
| 5 | Greenlight Radar / Parallel | 3.7 / 5 | Easy to demonstrate, but research agents are more likely to be crowded and feel generic. |
| 6 | Fan Cut Lab / Replit | 3.4 / 5 | Attractive UX, but creator/fan tools risk being read as novelty rather than enterprise workflow. |

## Product scope

### Target user and job

- **Primary user:** a script supervisor or assistant director.
- **Job:** understand the downstream impact of one proposed scene change before it creates a continuity or schedule problem.
- **Moment of use:** immediately after a revised script or call-sheet fact enters production.
- **Success:** the person receives one short, evidence-backed impact packet and creates the appropriate follow-up.

### Core workflow to build

1. Load the seeded six-scene production package: script excerpts, scene facts, call-sheet rows, and dailies notes.
2. Apply a revision to one named scene.
3. Gemini extracts the changed facts; store the version and source references in ClickHouse.
4. Query ClickHouse for affected scenes, already-shot scenes, and scheduled dependencies.
5. Run two deterministic checks: continuity mismatch and downstream-dependency impact.
6. Use Gemini to explain the evidence in plain English and draft one bounded follow-up.
7. The user creates that follow-up; save the decision, source evidence, and timestamp in ClickHouse.

### One unforgettable demo moment

Change Scene 12 from “blue jacket” to “black jacket” after Scene 11 has been shot with the blue jacket. SlateGuard immediately flags the continuity break, shows the three source records, identifies the two dependent scheduled shots, drafts a wardrobe/AD follow-up, and records the supervisor’s action.

### Explicitly cut

- Full computer-vision analysis of raw video or file uploads.
- Generating or editing film/video assets.
- Multiple partner tracks, multiple agents, or loosely connected integrations.
- Authentication, team collaboration, notifications, calendar synchronization, or autonomous production changes.
- A broad studio-management suite or generic chat experience.

## Architecture and evidence plan

| Layer | Purpose | Evidence for judges |
| --- | --- | --- |
| Gemini + Google Cloud Agent Builder | Structured extraction, explanation, agent orchestration | A visible agent run and documented code path using accepted Google Cloud SDKs. |
| ClickHouse | Source facts, scene versions, conflict queries, decision/audit events | The official `mcp-clickhouse` MCP server is connected to a cluster and invoked during the live demo. |
| Deterministic rules | Check facts across versions and sources | A transparent rule/evidence panel, not a hidden model judgment. |
| Hosted app | Operator console and project URL | A stable deployment judges can open. |

Use a fully synthetic, labeled package with six polished public-demo scenes and 15–20 revision fixtures with known expected findings. Track precision, recall, and review-time reduction within the test set; label them as prototype evaluation results. Do not expand the public product dataset merely to inflate scope.

## Design requirements

- A `Load demo production` starting screen and a scripted `Apply revision` control.
- One impact detail view with source excerpts, versions, and a clear “why this matters” statement.
- One human action: `Create follow-up`.
- A small append-only activity timeline.
- A graceful “insufficient evidence” state.
- No blank-page chatbot as the primary interface.

## Build schedule

| Dates | Outcome |
| --- | --- |
| Days 1–2 | Confirm ClickHouse/Gemini access; create six scenes, three seeded revisions, and labels for the two checks. |
| Days 3–5 | Build the schema, ClickHouse writes/queries, and the two deterministic checks. Make the core loop work before styling anything. |
| Days 6–7 | Add Gemini fact extraction/explanation, the impact view, and `Create follow-up` activity event. |
| Days 8–9 | Deploy hosted app; add a tiny evaluation script; correct false positives and broken empty states. |
| Days 10–11 | Refine UI, README, architecture diagram, public OSI license, and seeded demo reset. |
| Days 12–13 | Record the functional three-minute video, rehearse from a clean reset, and complete a submission dry run before the Sept. 7 deadline. |
| Remaining time | Buffer only: bug fixes, demo reliability, and submission polish. No new feature work after the clean rehearsal. |

## Three-minute video storyboard

| Time | Demonstration |
| --- | --- |
| 0:00–0:20 | Name the user, one production-change problem, and the concrete outcome. |
| 0:20–0:50 | Load the demo and apply the Scene 12 wardrobe revision. |
| 0:50–1:40 | Reveal the conflict, linked evidence, ClickHouse-backed dependency query, and deterministic checks. |
| 1:40–2:15 | Show the bounded Gemini explanation and `Create follow-up` action. |
| 2:15–2:40 | Show the persisted activity event plus prototype evaluation results. |
| 2:40–3:00 | Show the deployed product, Google Cloud and ClickHouse runtime integration, and outcome statement. |

## Pre-submit gates

- [ ] The official `mcp-clickhouse` MCP server is connected to a ClickHouse Cloud or self-hosted cluster, called at runtime in the main path, and easy to locate in the repository.
- [ ] Google Cloud/Gemini use is called at runtime and documented precisely.
- [ ] No prohibited non-Google AI model, agent framework, or AI API appears in the project, its runtime, or its development dependencies.
- [ ] Hosted app is publicly reachable and uses seeded demo data safely.
- [ ] Public repository includes all source, setup instructions, assets, and a visible OSI license.
- [ ] Video is public, in English or English-subtitled, and demonstrably functional rather than cinematic filler.
- [ ] Partner track is ClickHouse everywhere: Devpost form, pitch, video, README, and architecture.
- [ ] Required submission fields, repository URL, hosted URL, project-new/existing status, and original-work/data rights are accurate.
- [ ] No claim of production accuracy, savings, or legal readiness exceeds the prototype evidence.

## Pivot rule

By the end of Day 2, prove one real ClickHouse-backed write and dependency query in a deployed or deployment-ready app. If that fails, do **not** switch to a different product concept or chase a perceived easier track. Keep the same tiny change-impact workflow and only change partner tracks if an alternative integration is already validated. Entrant-count data has not been published in the official information reviewed, so competition is not a sound reason to pivot.
