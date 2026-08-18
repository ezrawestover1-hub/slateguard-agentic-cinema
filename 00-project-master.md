# SlateGuard — project master

> **North star:** Build a top-three-caliber ClickHouse-track submission for Agentic Cinema: a real, polished, evidence-first production change-control agent—not a generic AI demo.

---

## 1. Executive summary

### Product

**SlateGuard is version control for production reality.**

Film and television teams make constant creative revisions. A change to a costume, prop, location, line, scene timing, or character detail can silently affect footage already shot, future call sheets, department work, editorial context, and shoot readiness.

SlateGuard turns one revision into an evidence-backed **Change Packet**: it identifies the production blast radius, shows source evidence, recommends a bounded next action, and records a human decision so the production can move forward safely.

### Product promise

> Make the change. See the blast radius. Decide with evidence. Keep production moving.

### Selected contest expression

Submit to the **ClickHouse** track. The hackathon version focuses on one workflow:

```text
Load a six-scene fictional production
→ revise one scene fact
→ identify downstream continuity and schedule impacts
→ show evidence from the production record
→ create a human-approved follow-up
→ persist the decision and updated readiness state
```

---

## 2. Competition target

The target is **top three**, not “a good portfolio project.”

The submission must be something a judge can defensibly score at **94+ / 100** and explain in one sentence:

> “SlateGuard makes creative changes operationally safe by showing their evidence-backed impact before they reach the set, edit, or budget.”

### Top-three scoring target

| Area | Target | Evidence that earns it |
| --- | ---: | --- |
| Technological implementation | 24–25 / 25 | Real Gemini/Google Cloud agent behavior; official ClickHouse MCP queries and writes in the critical runtime path; deterministic checks; audit trail. |
| Design | 23–25 / 25 | A clear, premium operator workflow: change, evidence, impact, decision, readiness. No generic chat surface. |
| Potential impact | 23–24 / 25 | A specific production user and costly moment; a labeled evaluation set; careful, credible outcome claims. |
| Quality of idea | 23–24 / 25 | “Production change intelligence” / “Git for production decisions” is non-obvious and domain-aware. |

### Probability framing

There are 5,894 registered participants, but the official data does not reveal how many will submit, select ClickHouse, or qualify. Partner-track selection occurs at submission, so registration totals cannot forecast the ClickHouse field.

Assuming a fully compliant, unusually polished entry and a qualified ClickHouse field of roughly 150–225, a reasonable planning estimate is:

- Any prize: approximately 8–13%
- First place: approximately 3–5%

These are planning estimates, not measured odds. The controllable objective is to make the entry clearly real, useful, and memorable faster than competing projects.

---

## 3. Official event requirements and non-negotiables

The Devpost website/rules control if any event feed or helper disagrees.

### Deadline

- **Hard deadline:** 2:00 PM PT on **September 7, 2026**.
- Treat September 5 as the feature-freeze date.
- The official rules deadline conflicts with a later date returned by a separate event feed. Use the earlier deadline.

### What the project must be

- A functional, production-ready AI agent or multi-agent network for a real media-and-entertainment workflow.
- Powered by **Gemini** and **Google Cloud Agent Builder**.
- Enter exactly one partner track. This project targets **ClickHouse**.
- Run on web, Android, or iOS. SlateGuard will be a web app.

### ClickHouse requirement

- Use the official **`mcp-clickhouse`** MCP server at runtime.
- Connect it to a real ClickHouse Cloud or self-hosted cluster.
- The key user path must query/write through it. A mention in a README or an unused client does not qualify.

### AI tooling restriction

- Use Google Cloud AI tools and any built-in AI features of the selected partner only.
- Do **not** include other AI models, agent frameworks, or AI APIs in the project.
- Standard non-AI third-party services and ordinary web frameworks are not prohibited by this rule.

### Submission requirements

- Public hosted project URL.
- Public GitHub, GitLab, or Bitbucket repository with all code, assets, and runnable instructions.
- Visible OSI-approved open-source license.
- Public demo video of at most three minutes, in English or with English subtitles, showing the project functioning—not cinematic filler.
- Actual Google Cloud and ClickHouse runtime use clearly traceable in source code.
- Complete Devpost submission fields, including track selection and technology disclosures.
- Original, rights-cleared content and data. Use self-authored fictional production materials to avoid IP risk.

---

## 4. The product vision

### Category

SlateGuard is a **production change-intelligence system**. It is neither an AI scriptwriter nor an ordinary continuity checker.

It creates a durable link between:

- a creative revision;
- the original source facts;
- the scenes, footage, assets, departments, and shoot dates affected;
- the human decision that resolves the issue; and
- the readiness state of the production afterward.

### Target users

| User | Job to be done |
| --- | --- |
| Script supervisor | Prove whether a change conflicts with continuity and preserve intentional exceptions. |
| Assistant director | Understand whether an upcoming shoot is ready and who owns outstanding work. |
| Producer/coordinator | See high-impact change risk and get a concise decision packet. |
| Editor/post lead | Understand which decisions and changes affect available footage. |

### Core product surfaces

| Surface | Purpose |
| --- | --- |
| Production Pulse | Overview of shoot readiness, active risks, and decisions waiting on people. |
| Scene Ledger | Versioned source of truth for scene facts, story order, shooting order, assets, and evidence. |
| Change Packet | Focused review of one revision: what changed, what it affects, why, and what to do. |
| Production Blast Radius | Dependency map of the scene, footage, assets, departments, and scheduled work touched by a change. |
| Decision Room | Human action: create follow-up, approve, request revision, mark intentional variance, or escalate uncertainty. |
| Decision Memory | Durable history of who decided what, why, and the evidence considered. |
| Readiness Forecast | A preventative view of whether unresolved changes threaten the next shoot milestone. |

### Full ideal example

Maya’s wardrobe changes from a blue jacket to a black jacket in Scene 12.

SlateGuard shows:

1. The old and new scene versions.
2. Scene 11 dailies that show the blue jacket already filmed.
3. Two scenes on tomorrow’s call sheet that still specify blue.
4. The wardrobe, AD, editorial, and shoot-readiness impact.
5. A bounded follow-up packet with evidence and an owner.
6. The supervisor’s decision: follow-up created, intentional variation approved, or revision requested.
7. The preserved decision history so the issue is not rediscovered later.

---

## 5. Hackathon scope: build this and nothing more

This is a solo-builder project. The advantage is a flawless thin slice, not feature breadth.

### Scope rule

> One agent, one user, one revision workflow, one fictional production dataset, and one consequential human decision.

### In scope

- Six self-authored fictional scenes.
- Script excerpts, scene facts, call-sheet rows, and dailies notes.
- One revision control: wardrobe, prop, location, time-of-day, or dialogue fact changes.
- Two deterministic impact checks:
  1. continuity mismatch;
  2. already-shot or scheduled downstream dependency.
- Gemini/Google Cloud Agent Builder extracts facts and explains the evidence.
- Official `mcp-clickhouse` retrieves dependencies and stores version/audit events.
- One human action: **Create follow-up**.
- Updated readiness state.
- A graceful “insufficient evidence; review required” state.

### Out of scope

- Raw video analysis, video upload, or broad computer vision.
- General chat UI.
- Multiple agents for their own sake.
- Multiple partner tracks or integrations.
- Authentication, team collaboration, notifications, or calendar sync.
- Full scheduling, budget management, or studio management.
- Autonomous production changes.
- Broad role-specific dashboards.
- What-if simulation in the first submission.

---

## 6. The core user experience

### Change Packet flow

```text
1. User loads the demo production.
2. User applies a revision to Scene 12: blue jacket → black jacket.
3. SlateGuard displays the diff and source version.
4. The agent retrieves related records using the official ClickHouse MCP.
5. Deterministic checks identify conflicts/dependencies.
6. Gemini explains the evidence and drafts a bounded follow-up.
7. User creates the follow-up.
8. SlateGuard persists the decision and changes readiness status.
```

### The unforgettable 30-second moment

The user applies the revision. The interface immediately shows:

> “This change conflicts with footage already shot in Scene 11 and affects two scenes scheduled tomorrow.”

The source evidence, dependency query result, affected scenes, and human action must all appear in one elegant sequence.

### Interface principles

- No blank chatbot screen.
- One primary question per screen.
- Progressive disclosure: immediate answer first, source evidence on demand.
- Every claim is linked to source evidence.
- Clearly distinguish confirmed facts, inference, intentional variation, and missing evidence.
- Use human production language, not AI jargon.
- Premium visual language: slate black, warm ivory, production green, review amber, spare urgent red.

---

## 7. Data and intelligence model

### Core data objects

- Production
- Scene; story order and shooting order
- Script version/revision
- Character, wardrobe, prop, location, time-of-day, dialogue facts
- Call-sheet/schedule row
- Dailies or asset note
- Source record/version/timestamp
- Change request
- Dependency and triggered check
- Impact finding
- Human decision/follow-up/audit event
- Readiness state

### Agent responsibilities

- Parse a revised scene fact.
- Retrieve version history and connected production records.
- Explain why the deterministic rules triggered.
- Write a concise, evidence-grounded impact packet.
- State uncertainty and request review where source data is incomplete.

### Deterministic responsibilities

- Version history and data integrity.
- Relationship/dependency lookup.
- Continuity-mismatch check.
- Already-shot/scheduled-dependency check.
- Decision ownership and audit log.

### Trust standard

Every material finding must expose:

- its source record(s);
- source version and timestamp;
- triggered rule/dependency path;
- evidence completeness/confidence;
- the difference between fact, inference, and uncertainty.

Never allow the product to sound certain when the data is incomplete.

---

## 8. Technical proof and evaluation

### Judge-visible runtime proof

The demo must show all five links:

```text
Revision
→ official mcp-clickhouse dependency query
→ source-evidence result
→ Gemini-backed Change Packet
→ human follow-up + ClickHouse persisted readiness update
```

Add a compact **Live Evidence Trace** panel during the demo showing the query/result, evidence IDs, action, and saved event. It should clarify—not overwhelm—the product narrative.

### Prototype evaluation

Create 15–20 labeled revisions across wardrobe, props, location, time-of-day, and dialogue.

Measure and show:

- known conflicts surfaced;
- false positives;
- evidence coverage (findings with source links);
- time to a reviewable follow-up;
- unresolved high-impact changes before/after resolution.

Describe all numbers as prototype evaluation results. Do not invent commercial savings.

### Data safety

- All scripts, call sheets, dailies notes, names, locations, and assets are self-authored fictional material.
- No copyrighted media, real actor likenesses, confidential production materials, or unlicensed third-party data.

---

## 9. Demo and narrative

### Three-minute video structure

| Time | What the judge sees |
| --- | --- |
| 0:00–0:20 | “Creative changes are normal. Hidden operational blast radius is the problem.” Identify the script supervisor/AD user. |
| 0:20–0:45 | Load the production and change Scene 12’s jacket from blue to black. |
| 0:45–1:30 | Live dependency query, evidence records, and the conflict against already-shot/scheduled material. |
| 1:30–2:05 | Clear Change Packet, Gemini explanation, and Create Follow-up decision. |
| 2:05–2:30 | Persisted decision/audit event and revised shoot-readiness signal. |
| 2:30–3:00 | Briefly prove Google Cloud + official ClickHouse MCP runtime architecture, prototype metrics, hosted app, and final product promise. |

### Spoken pitch

> Creative changes are normal on a production. The problem is that a single change can quietly affect footage already shot, tomorrow’s call sheet, wardrobe, editorial, and the budget. SlateGuard is version control for production reality. It turns a revision into an evidence-backed, human-approved operational decision. Change the scene, see the blast radius, decide with evidence, and keep production moving.

### Project-page positioning

> SlateGuard uses Gemini and a ClickHouse-backed production memory to transform a creative revision into a traceable Change Packet. It identifies the affected scenes and departments, cites the evidence, guides a human-approved follow-up, and keeps upcoming shoot readiness visible.

---

## 10. Submission-standard checklist

### Compliance

- [ ] Submit before 2:00 PM PT on Sept. 7, 2026.
- [ ] Use Gemini/Google Cloud Agent Builder and permitted Google Cloud AI only.
- [ ] Use the official `mcp-clickhouse` server against a real ClickHouse Cloud or self-hosted cluster.
- [ ] Select ClickHouse as the Devpost track.
- [ ] Confirm all data/assets are self-authored or rights-cleared.
- [ ] Confirm all form fields are accurate, including participant, residency, and project-status information.

### Product proof

- [ ] Hosted web application is publicly reachable.
- [ ] Main demo path works from a clean reset.
- [ ] Revision, ClickHouse query, source evidence, agent explanation, decision, and readiness update are real.
- [ ] “Insufficient evidence” behavior exists.
- [ ] Fifteen to twenty labeled evaluation cases run consistently.

### Repository proof

- [ ] Public repository includes all code, self-authored demo assets, and clear setup instructions.
- [ ] OSI-approved license is visible and detectable.
- [ ] README names the exact Google Cloud and ClickHouse components and points to their runtime code paths.
- [ ] Repository is free of prohibited AI dependencies.
- [ ] A judge can reproduce the demo or understand the hosted configuration with minimal friction.

### Video proof

- [ ] Public video is three minutes or less and English/English-subtitled.
- [ ] It shows real functioning product behavior, not only slides or cinematic montage.
- [ ] It leads with the user problem and Change Packet—not architecture.
- [ ] It visibly demonstrates the official ClickHouse MCP and Google Cloud runtime story.

---

## 11. Risks and decisions

| Risk | Response |
| --- | --- |
| Field may be much larger than expected | Do not optimize for hypothetical entrant count; optimize for unmistakable proof and clarity. |
| ClickHouse setup/integration becomes difficult | Prove a real `mcp-clickhouse` write and dependency query by Day 2. Do not build decorative UI before this works. |
| Product becomes generic continuity checking | Preserve the “creative revision → operational blast radius → accountable decision” framing in every screen and sentence. |
| Agent makes unsupported assertions | Show sources, deterministic rule paths, and “review required” states. |
| Scope grows beyond a solo build | Keep only one end-to-end Change Packet loop; every additional surface is a luxury. |
| Visual demo looks like a data dashboard | Design the evidence reveal and blast radius as the main visual story, with minimal surrounding UI. |
| Submission fails a baseline screen | Use the checklists above; do a full submission dry run before feature freeze. |

---

## 12. Ideal future product, after the hackathon

Do not build these for the first submission unless the core loop is already excellent.

- Role-aware views for script supervisor, AD, producer, and editor.
- Formal intentional-variation workflows and decision memory across the entire production.
- What-if simulation: retain original continuity vs. accept a variation vs. reshoot/revise.
- Controlled multimodal evidence from approved dailies stills/storyboard frames.
- Department-ready action packets with deadline, owner, and source links.
- Production Readiness Forecast across multiple upcoming shoot days.
- Integrations with scheduling, asset management, VFX review, editorial, rights, and budgeting systems.

The ideal product is not “AI for filmmaking.” It is the **production operating system for accountable creative change**.

---

## 13. Final decision rule

When choosing between any two implementation ideas, prefer the one that makes this sequence more real, more visible, or more reliable:

```text
Creative revision
→ ClickHouse-backed evidence and dependency query
→ understandable production blast radius
→ human-owned decision
→ durable production memory and readiness update
```

Everything else is optional.

---

## 14. Eight-sprint solo build map

Each sprint is one command chunk in chat. Complete and verify it before advancing. The project should remain demonstrable after every sprint.

| Sprint | Goal | Definition of done |
| --- | --- | --- |
| 1. Compliance and runtime spike | Prove the required stack before designing the product. | A minimal web/app backend can call permitted Gemini/Google Cloud tooling and the official `mcp-clickhouse` server against a real cluster; the calls and results are visible locally. Stop or fix access here before building UI. |
| 2. Production memory | Create the self-authored six-scene fictional production dataset and its versioned data model. | Scenes, facts, call-sheet rows, dailies notes, source versions, dependencies, and audit events are seeded in ClickHouse and can be read back. |
| 3. Revision and blast radius | Implement the true product engine: one revision produces evidence-backed impacts. | A Scene 12 blue-jacket → black-jacket revision creates a persisted version and returns the already-shot and scheduled downstream records through `mcp-clickhouse`; two deterministic checks pass. |
| 4. Agentic Change Packet | Turn raw impact records into a trustworthy operator brief. | Gemini/Google Cloud Agent Builder extracts/normalizes the changed fact, cites retrieved evidence, explains the impact, and exposes a clear “insufficient evidence” state. |
| 5. Product interface | Build the polished three-screen experience. | User can load demo data, apply a revision, inspect the Change Packet/evidence/blast radius, and create one follow-up without a chat-first interface. |
| 6. Decision memory and readiness | Close the loop and make the product feel operational. | The follow-up is persisted, source evidence and rationale are retained, and a visible readiness status changes as the issue is resolved. |
| 7. Reliability and deployment | Make the build judge-safe. | Fifteen to twenty labeled evaluation cases run; error/empty states work; hosted web app, public repo, setup instructions, and OSI license are ready. |
| 8. Submission package | Turn the working product into a winning entry. | Three-minute functional video, screenshots, project write-up, runtime-proof README, Devpost fields, and final compliance check are complete before the official deadline. |

### Command rhythm

- Say **“next”** to begin the next sprint.
- Within a sprint, build and verify the stated definition of done; do not add future-sprint features.
- At the end of every sprint, record what works, what failed, and whether the core demo still runs.
- Sprint 1 is a hard gate: no UI work until Gemini/Google Cloud and official `mcp-clickhouse` runtime calls are confirmed.

---

## 15. Twenty-one-sprint execution sequence

Use this sequence when advancing one `next` at a time. A sprint should normally be a focused 45–120 minute work block. Do not advance until its acceptance condition is true.

| # | Sprint | Build focus | Acceptance condition |
| ---: | --- | --- | --- |
| 1 | Rules lock | Record the contest constraints in the repository: Sept. 7 deadline, Google-only AI, official `mcp-clickhouse`, public OSS submission. | A `CONTEST.md` or equivalent checklist exists; no prohibited AI tool is part of the planned runtime. |
| 2 | Project shell | Create the application repository, web-app shell, configuration pattern, and local run command. | The empty app starts locally with one documented command. |
| 3 | Google runtime spike | Connect permitted Gemini/Google Cloud Agent Builder tooling and run one trivial allowed call. | A visible, logged Google runtime response succeeds from the app/backend. |
| 4 | ClickHouse MCP spike | Configure official `mcp-clickhouse` against a real ClickHouse cluster and run a test query. | A visible, logged MCP query succeeds; configuration is documented without committing secrets. |
| 5 | End-to-end technical spike | Call Google tooling and ClickHouse MCP from the same thin application path. | One route/action proves both required integrations work together. |
| 6 | Fictional production bible | Author the six-scene fictional production: story order, shooting order, characters, wardrobe, props, call-sheet rows, and dailies notes. | All demo material is original, internally consistent, and safe to publish. |
| 7 | Production-memory schema | Define/store scene facts, source records, versions, dependencies, findings, decisions, and readiness events. | Seed data writes to ClickHouse and can be read back as structured records. |
| 8 | Scene Ledger | Build the read view/API for one scene and its source facts/versions. | Scene 12 shows its current facts, prior version, and linked source records. |
| 9 | Revision command | Implement the one supported revision: blue jacket → black jacket for Scene 12. | Applying the revision creates an immutable new version and preserves the old version. |
| 10 | Dependency query | Query the versioned production memory for records connected to the revised fact. | The query returns Scene 11’s dailies evidence and the scheduled dependent scenes. |
| 11 | Continuity rule | Implement deterministic check one: identify a mismatch against already-shot footage. | The known Scene 11/12 wardrobe conflict is found with evidence IDs. |
| 12 | Schedule-impact rule | Implement deterministic check two: identify future scheduled work affected by the revision. | The known dependent call-sheet scenes are returned with status and shoot relevance. |
| 13 | Evidence Trace | Make the runtime chain inspectable: input revision, MCP query/result, source evidence, checks, and saved events. | A compact trace proves the finding without exposing secrets or overwhelming the user. |
| 14 | Fact extraction agent | Use permitted Gemini/Google tooling to normalize the revised scene fact into the expected schema. | A valid changed-fact record is generated, validated, and stored; malformed input is handled. |
| 15 | Change Packet agent | Generate a concise, grounded explanation and bounded recommended follow-up from retrieved evidence. | The output names the specific conflict, evidence, affected work, and safe next action. |
| 16 | Uncertainty and abstention | Add the “insufficient evidence; human review required” behavior. | Missing/contradictory source data never produces a false confident conclusion. |
| 17 | Change Packet UI | Build the central product screen: diff, severity, evidence, impact, and recommendation. | A nontechnical user can understand the scenario and its consequence in under 30 seconds. |
| 18 | Blast Radius UI | Add the memorable visual representation of affected scenes, footage, departments, and schedule. | Every node corresponds to queryable source evidence; the view clarifies rather than decorates. |
| 19 | Human decision + readiness | Add `Create follow-up`, audit event persistence, and a visible change to shoot readiness. | A decision is stored in ClickHouse and the Production Pulse reflects the resolved/pending state. |
| 20 | Quality and deployment | Run 15–20 labeled scenarios, repair weak paths, deploy the hosted app, and make the public repository reproducible. | Evaluation results, hosted demo, public source, OSI license, setup instructions, and clean error states are ready. |
| 21 | Submission proof | Produce the final video, screenshots, Devpost copy, and end-to-end compliance review. | The 3-minute video proves revision → MCP query → evidence → decision → readiness; submission is ready before deadline. |

### Sprint grouping

| High-level phase | Detailed sprints |
| --- | --- |
| Compliance and runtime spike | 1–5 |
| Production memory | 6–8 |
| Revision and blast radius | 9–13 |
| Agentic Change Packet | 14–16 |
| Product interface and decision loop | 17–19 |
| Reliability, deployment, and submission | 20–21 |
