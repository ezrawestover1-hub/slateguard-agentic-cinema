# SlateGuard — ideal product brief

## One-line thesis

**SlateGuard is version control for production reality.** It turns every creative revision in a film or television production into an evidence-backed, human-approved operational decision before it becomes rework, a missed shoot-day dependency, or an editorial surprise.

## Product category

SlateGuard is not an AI screenwriter, a generic production chatbot, a task tracker, or a continuity checker that merely highlights mismatches.

It is a **production change-intelligence system**: the control layer between a creative decision and the people, footage, assets, schedules, and departments that decision affects.

Its core question is:

> A change was made. What does it affect, what evidence supports that conclusion, who must decide, and what is the approved next action?

## The problem

Film and television productions are networks of connected decisions. A fact in one scene—costume, prop, dialogue, location, time of day, actor availability, VFX requirement, or story timing—can be linked to footage already shot, future scenes, call sheets, department work, editing context, rights records, and budget decisions.

Creative change is normal and necessary. The operational failure is **change without shared context**.

Today, the change impact often lives in a mix of personal memory, PDF markup, spreadsheets, email, call sheets, meetings, messaging apps, and departmental silos. The result is late discovery of continuity problems, duplicate manual review, unclear ownership, avoidable pickups, and decisions whose rationale disappears.

SlateGuard creates a durable, explainable change record that the production can trust.

## Users and jobs to be done

### Script supervisor

They need to preserve continuity and document intentional variations across story order and shooting order.

**Job:** “When something in a scene changes, help me prove whether it conflicts with footage or planned scenes, and preserve the decision I make.”

### Assistant director

They need to protect shoot readiness and coordinate the work created by a change.

**Job:** “Before the next call sheet locks, show me whether a change creates a blocker, who owns it, and whether it has been resolved.”

### Producer or production coordinator

They need to understand operational risk and ensure decisions have accountable owners.

**Job:** “Show me the change risks that can affect the next shoot day and give me a concise, evidence-backed decision packet.”

### Editor or post-production lead

They need to know which creative decisions affect available footage and editorial continuity.

**Job:** “Tell me which unresolved changes affect the scenes or assets I am cutting, and why.”

## The finished-product promise

SlateGuard lets a production team make creative changes with confidence.

> Make the change. See the blast radius. Decide with evidence. Keep the production moving.

The product should feel like a calm, premium production command center: cinematic in visual language, but completely practical in interaction. It should never feel like a chat demo that asks the user to formulate the right prompt.

## Core operating model: the production change graph

SlateGuard models a production as a time-aware graph of versioned facts and dependencies.

### First-class records

- Production
- Scene, story order, and shooting order
- Script version and scene revision
- Character, costume, prop, location, vehicle, and time-of-day facts
- Call-sheet and scheduled-shoot information
- Dailies, takes, stills, shot notes, and editorial references
- Assets and department work items
- Change request
- Detected impact
- Source evidence
- Human decision, owner, rationale, and timestamp

### Key relationship types

- “Scene 13 follows Scene 12 in the story”
- “Shot A was filmed using costume state B”
- “Scene 14 is scheduled for the next shoot day”
- “Wardrobe task C exists because of scene fact D”
- “Creative change E supersedes version F”
- “Decision G intentionally accepts otherwise conflicting evidence”

The graph allows SlateGuard to distinguish a harmless revision from a change with real downstream consequences.

## Product surfaces

### 1. Production Pulse

The home view is an operational picture of the production, not a chat interface.

It shows:

- Shoot-day readiness: clear, attention needed, or blocked
- Unresolved high-impact changes
- Decisions awaiting human review
- Scenes with recently changed source facts
- Department queues and ownership status
- A concise summary of what could affect the next production milestone

The user should be able to open the product and understand the state of production in seconds.

### 2. Scene Ledger

The Scene Ledger is the authoritative history of a scene.

It presents the current canonical scene facts alongside their prior versions, source documents, dailies references, associated assets, planned shoot details, and recorded decisions. It preserves story order and shooting order simultaneously, because those two perspectives often create different continuity risks.

### 3. Change Packet

The Change Packet is SlateGuard’s central interaction.

When a change occurs, the user sees:

- The old value and the new value
- Who made the change and when
- The specific scenes, assets, footage, departments, and decisions affected
- The exact evidence and source excerpts behind every impact claim
- Severity and readiness implications
- A bounded recommended resolution
- A human decision control

The packet should read like the best possible production brief: short, structured, verifiable, and actionable.

### 4. Production Blast Radius

This is the memorable visual surface.

A change sits at the center of a dependency map. The map radiates to connected scenes, footage, props, costumes, departments, shoot dates, and decisions. Nodes show state: already shot, scheduled, approved, pending, conflicted, or intentionally varied.

For example:

```text
Scene 12: Maya’s wardrobe changes from blue jacket to black jacket
├─ Scene 11: already shot — blue jacket appears in dailies
├─ Scene 13: scheduled — call sheet still specifies blue jacket
├─ Scene 14: scheduled — direct story-continuity dependency
├─ Wardrobe: follow-up required
├─ Assistant director: next call-sheet review required
└─ Editorial: continuity context updated
```

The map should be an explanation tool, not decorative data visualization. Each node must lead to inspectable evidence.

### 5. Decision Room

SlateGuard does not autonomously change a shoot schedule or issue a production directive. It prepares a decision and leaves consequential action under human control.

Possible decisions include:

- Create follow-up
- Assign department owner
- Approve a proposed resolution
- Request a revision
- Mark as intentional variation
- Escalate because evidence is incomplete

Every decision records a rationale, owner, timestamp, evidence set, and resulting follow-up.

### 6. Decision Memory

The system retains not only changes but the reason a team accepted or rejected them.

Example:

> “The black jacket is an intentional story-time jump. Wardrobe and editorial confirmed the transition; the variation was approved by the script supervisor on Aug. 21.”

This prevents the same ambiguity from being rediscovered repeatedly and creates institutional memory across the production lifecycle.

### 7. Readiness Forecast

SlateGuard should move beyond finding individual issues to predicting readiness.

Examples:

- “Tomorrow’s shoot has two unresolved changes affecting three scheduled scenes.”
- “The rooftop sequence is at risk because one location revision has not reached lighting and art departments.”
- “All high-impact changes for the next shoot day have owners or approved exceptions.”

The product becomes a preventative operational system rather than a retrospective audit tool.

## Example experience

A producer revises Scene 12: Maya’s wardrobe changes from a blue jacket to a black jacket.

SlateGuard creates a Change Packet:

1. It displays the exact old and new facts.
2. It identifies that Scene 11 was already filmed with the blue jacket.
3. It finds two future scenes, scheduled for tomorrow, whose call-sheet data still expects blue.
4. It shows all three source records side by side.
5. It flags the likely continuity break and the next-shoot readiness risk.
6. It recommends a bounded action packet for Wardrobe and the AD.
7. The script supervisor creates the follow-up, or marks the variance intentional with an explanation.
8. The decision enters the production’s durable history.

The experience is not “the model noticed something.” It is “the production has a reliable, accountable decision.”

## Intelligence and trust model

SlateGuard should be intelligent, but it should be even more trustworthy.

### What the agent does

- Extracts structured production facts from a revision or source document
- Retrieves related versions, dependencies, and decisions
- Synthesizes an impact explanation from source evidence
- Produces a constrained, role-specific follow-up recommendation
- Detects incomplete, ambiguous, or contradicting data and escalates it

### What must remain deterministic

- Version history
- Dependency relationships
- Rule-triggered conflicts
- Access/role boundaries
- Decision ownership and audit records

### Required evidence behavior

Every material claim should have:

- Source record(s)
- Source version and timestamp
- Confidence or evidence completeness
- The triggered rule or dependency path
- A clear distinction between confirmed fact, inference, and missing data

SlateGuard earns trust by saying “review required” when it cannot establish the facts. False certainty is more damaging than a visible escalation.

## Ideal technical/product behavior

Gemini and Google Cloud Agent Builder provide the agentic reasoning layer: parsing revisions, extracting facts, retrieving evidence, composing an explanation, and structuring the change packet. For the contest build, use only permitted Google Cloud AI tooling; the rules prohibit other AI models, agent frameworks, and AI APIs.

ClickHouse provides the operational memory and fast analytical layer: versioned scene facts, source references, dependency relationships, impact queries, decision logs, and readiness aggregation. For the ClickHouse track, the core user path must use the official `mcp-clickhouse` MCP server connected to ClickHouse Cloud or a self-hosted cluster; generic mention or an unused client is insufficient.

The most important technical behavior is **time-aware change impact**:

> “What did the production believe before this revision, what is true now, what was already shot, what is scheduled, and which decisions remain unresolved?”

## Visual and interaction direction

SlateGuard should look like a premium production instrument rather than generic enterprise software.

- Base palette: slate black, warm paper/ivory, production green, review amber, urgent red used sparingly
- Typography: editorial/cinematic headings with practical high-legibility body text
- Layout: one primary question per screen; progressive disclosure for evidence and graph detail
- Motion: subtle state transitions that clarify a change moving through review and resolution
- Language: short, decisive, human production language—not model-centric jargon
- Accessibility: high contrast, keyboard support, no color-only severity signals, readable evidence excerpts

## Distinctive features in the full ideal product

### Intentional variation

Not every mismatch is a mistake. A team can formally approve an intended change and preserve the rationale, preventing repetitive false alerts while maintaining editorial context.

### What-if decision simulation

For an important change, SlateGuard compares bounded choices:

- Keep original continuity
- Accept an intentional variation
- Reshoot or revise affected scenes

For each, it shows impacted scenes, departments, decisions, and readiness consequences. This is decision support, not autonomous production planning.

### Role-aware views

- Script supervisor: continuity evidence and exceptions
- AD: upcoming shoot readiness and assigned work
- Producer: risks, approvals, and milestone impact
- Editor: footage context and unresolved creative decisions

### Source integrity controls

Facts are visibly marked confirmed, inferred, disputed, or missing. Users can see their origin and recency rather than treating production data as universally reliable.

## Defensibility

SlateGuard is defensible because the value is not a generic model response. It is the accumulated, production-specific relationship between versions, evidence, decisions, and outcomes.

The more a production uses it, the more valuable its decision memory becomes: it learns what was intentionally changed, how exceptions were resolved, and what departments depend on what production facts.

## Value and success measures

The product should avoid unsupported financial claims. Its initial measurable value should be operational:

- Time from creative revision to accountable follow-up
- Percentage of known impact cases surfaced before the next shoot milestone
- Evidence coverage: findings with linked source records
- Number of unresolved high-impact changes before a shoot-day lock
- Time required for a supervisor to review a change versus manual cross-document review
- Rate of correctly preserved intentional variations

For a prototype, these should be measured against a labeled, synthetic or permissibly sourced production dataset and described transparently as prototype evaluation results.

## Hackathon product expression

For Agentic Cinema, the most credible narrow expression is not the entire ideal platform.

### Hackathon thesis

**SlateGuard turns a single production revision into an evidence-backed impact packet before it becomes rework.**

### Required finished demo loop

1. Load a small fictional production with six scenes, scene facts, call-sheet rows, and dailies notes.
2. Apply one revision to a costume, prop, time-of-day, location, or dialogue fact.
3. Show the old and new version.
4. Query the versioned production record for downstream dependencies.
5. Detect two deterministic impact types: continuity mismatch and already-shot/scheduled dependency.
6. Present evidence plus a short agent explanation.
7. Create one human-approved follow-up.
8. Save the decision and show the updated readiness state.

### Explicit non-goals for the hackathon version

- Raw video or broad computer-vision analysis
- Multiple agents for their own sake
- Multiple partner tracks
- Authentication, collaboration, notifications, or calendar synchronization
- Full studio management
- Autonomous schedule/production action
- Generic conversational interface

### Compliance-critical boundaries

- Submit by the earlier official-rules deadline: **2:00 PM PT on Sept. 7, 2026**. A separate event date feed exposed a later value, so the rules deadline is the safe controlling date.
- Use the official `mcp-clickhouse` MCP server at runtime against a real ClickHouse cluster.
- Use Gemini/Google Cloud Agent Builder and permitted Google Cloud AI tools only; do not include other AI models, agent frameworks, or AI APIs.
- Use original, rights-cleared production data and assets. A fictional, self-authored production dataset is the safest path.
- Provide a working hosted app, public open-source repository, visible OSI-approved license, reproducible instructions, and a public functional video of at most three minutes.

## Judge-facing position

The strongest concise description is:

> SlateGuard is version control for production reality. When a creative decision changes, it uses Gemini and a ClickHouse-backed production memory to show the operational blast radius, cite the evidence, and guide a human-approved response before the change reaches the set, edit, or budget.

It aligns with the event’s scoring dimensions:

- **Technological implementation:** real Gemini/Google Cloud agent behavior plus runtime ClickHouse queries/writes
- **Design:** a complete, evidence-first workflow instead of a proof-of-concept chat screen
- **Potential impact:** a concrete workflow for a defined media-production user
- **Quality of idea:** a non-obvious product category: production change intelligence

## Three-minute pitch narrative

### Opening

“Creative changes are normal on a production. The problem is that a single change can quietly affect footage already shot, tomorrow’s call sheet, wardrobe, editorial, and the budget.”

### Product reveal

“SlateGuard is version control for production reality. It turns a creative revision into an evidence-backed, human-approved operational decision.”

### Demonstration

“Maya’s jacket changes from blue to black in Scene 12. SlateGuard shows the previous and current scene versions, finds already-shot footage in Scene 11, identifies two scenes scheduled tomorrow, and creates a department-ready follow-up.”

### Trust and technology

“Every finding links to source evidence. Gemini structures and explains the change; ClickHouse holds the versioned production memory and returns the live dependency queries. A human owns the final decision.”

### Closing

“SlateGuard lets teams make creative changes without losing operational control: make the change, see the blast radius, decide with evidence, and keep production moving.”

## Questions another analysis should test

1. Is production change control the best sharp pain point for this event and a solo builder, or is another partner-track wedge stronger?
2. Which ClickHouse integration pattern most clearly proves that runtime use is indispensable while remaining simple enough for the hackathon?
3. What data model and two deterministic rules make the demo feel real without requiring raw video or copyrighted production materials?
4. What prototype evaluation method would make the impact claim credible to judges?
5. What exact product screens create the best “30-second understanding” and “one unforgettable visual” moments?
6. What should be omitted to maximize polish and reliability for a solo build?
