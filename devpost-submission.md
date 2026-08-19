# SlateGuard — Evidence Before Action

## Devpost one-line pitch

SlateGuard turns a film-production revision into ClickHouse-backed evidence, a bounded Gemini Change Packet, a human-owned follow-up, and a reader-verified readiness receipt.

## Description

### The problem

Production changes rarely stay isolated. A request as small as changing Scene 12's wardrobe from a blue jacket to a black jacket can conflict with already-shot dailies, affect the next call sheet, and require coordinated action from Wardrobe and the Assistant Director. The information usually exists, but across notes, production records, and schedules that are hard to consult under time pressure. That is how a creative change becomes a continuity or shoot-day risk.

### What SlateGuard does

SlateGuard is an evidence-first Continuity Command Desk for that decision. A script supervisor applies a prepared Scene 12 wardrobe revision. SlateGuard then:

1. writes the typed revision event through a constrained **ClickHouse writer MCP** path;
2. retrieves only the relevant, current production context through a separate read-only **ClickHouse reader MCP** path;
3. uses deterministic rules to identify the continuity conflict and downstream scheduled dependencies;
4. asks a schema-constrained Gemini Change Packet agent to explain only the supplied evidence; and
5. lets the human supervisor create the follow-up. The system writes that decision, then reads it back through the reader path before displaying a readiness receipt.

The built demo uses six self-authored fictional scenes. Its one judge-visible loop is deliberately narrow: **blue jacket → black jacket** in Scene 12, Scene 11 dailies and two upcoming dependencies as evidence, a Wardrobe + Assistant Director follow-up, and the verified transition from **At risk** to **Follow-up created**.

### Why ClickHouse is essential

SlateGuard treats ClickHouse as time-aware production memory, not background storage. Before an agent explains a change, the Impact Pulse queries only the established Scene 11 history, active Scene 12 revision, and the next scheduled dependencies. Archive, unrelated, and unscheduled records are excluded by the fixed reader-MCP queries before they reach the agent.

The ClickHouse integration is visible in the core loop:

```text
revision → writer MCP → reader MCP evidence → Gemini explanation → human decision → writer MCP → reader-verified receipt
```

The browser and model never receive raw database credentials or arbitrary SQL. Reader and writer processes use separate identities: the reader is limited to curated views, and the writer only appends named event records. The agent is an explanation layer, not an authority layer.

### Gemini and Google Cloud Agent Builder

The Change Packet uses Google ADK and Gemini with a structured response schema. It receives bounded facts, approved evidence IDs, deterministic findings, and allowed owners—not general database access. Its output is rejected if it cites unsupported evidence, changes a deterministic decision state, or recommends an unapproved owner. When the model path is unavailable or invalid, the product falls back to factual deterministic copy rather than inventing a claim.

The hosted application runs on Google Cloud Run. The project also includes the deployed Google Agent Runtime / Vertex AI Change Packet path used for the Gemini structured-output proof. Cloud-managed configuration keeps the runtime secrets outside the browser and source repository.

### What makes it different

SlateGuard is not a generic production chatbot or dashboard. It makes the sequence of authority unmistakable:

- **Evidence before action:** source records and deterministic impact come before the follow-up control.
- **Curated agent context:** the agent can explain the current decision window without receiving stale or irrelevant production memory.
- **Human ownership:** the consequential production task is created by the supervisor, not the model.
- **Verified closure:** a decision receipt is shown only after the durable follow-up and readiness event are read back through the protected reader path.

### Testing and verification

- 40 backend tests cover the API contracts, fixed ClickHouse MCP boundary, production-memory parsing, session/idempotency behavior, and Change Packet validation.
- The official Python `mcp-clickhouse` integration was verified with real reader → writer → reader behavior, including negative permission checks.
- The six-scene fictional schema and curated ClickHouse views support the exact Scene 12 evidence path shown in the product.
- A deployed Gemini structured Change Packet proof validates citations, deterministic status, and the allowed Wardrobe + Assistant Director recommendation.
- The public Cloud Run app was exercised through revision persistence, reader evidence retrieval, grounded Change Packet validation, human follow-up, and reader-verified receipt.

### Built with

React, TypeScript, Vite, Python, FastAPI, Google Cloud Run, Vertex AI / Google ADK / Gemini, Google Agent Runtime, ClickHouse Cloud, official `mcp-clickhouse`, Docker, Cloud Build, and GitHub Actions-compatible project tooling.

## Links

- **Hosted project:** https://sprint2---slateguard-vseh3ye7mq-uc.a.run.app
- **Open-source repository:** https://github.com/ezrawestover1-hub/slateguard-agentic-cinema
- **License:** MIT (visible in the repository)
- **Demo video:** **TODO — upload the final 2:20 functional, captioned cut to publicly visible YouTube or Vimeo, then paste the URL here.** Local render: `slateguard-demo-video/out/slateguard-judge-cut-140s.mp4`.

## Demo-video rundown (2:20)

| Time | Judge sees | It proves |
| --- | --- | --- |
| 0:00–0:10 | The costly production-change problem | Specific media-and-entertainment use case |
| 0:10–0:30 | Command Desk and prepared Scene 12 revision | A complete product surface, not a chat mockup |
| 0:30–0:50 | Guided live-workspace tour | The evidence, decision, owner, and readiness areas are usable |
| 0:50–1:10 | ClickHouse reader query / Impact Pulse | Relevant, current context is filtered before the agent reasons |
| 1:10–1:30 | Writer → reader → Change Packet trace | Partner technology is indispensable to the core loop |
| 1:30–1:50 | Human follow-up and read-back receipt | Human authority plus durable verified closure |
| 1:50–2:20 | Agent-memory architecture and close | Secure, credible design and product impact |

The render has English on-screen captions. A natural voiceover will be mixed to the same timing before upload.

## Screenshot plan

1. **Command Desk, before action** — revision, current readiness, and dominant Apply Revision action.
2. **Evidence and decision brief** — relevant source records, deterministic risk, owners, and explanation.
3. **Live trace** — writer persistence, reader retrieval, and Change Packet validation.
4. **Decision receipt** — human-created follow-up and reader-verified readiness transition.
5. **Impact Pulse** — bounded ClickHouse relevance counts before the change is applied.

Use the live captures already in `docs/demo-captures/`; do not upload older dark-shell design references.

## Devpost required-field worksheet

These values are ready to paste, except entries marked **confirm**. Do not submit the form until the video URL and all confirmations are complete.

| Devpost field | Draft answer |
| --- | --- |
| Submitter Type | Individual |
| Organization name | N/A |
| Government employee | **Confirm before submit** |
| Country of residence | United States — **confirm before submit** |
| Canada province | N/A |
| Project new or existing prior to July 27, 2026? | New |
| Partner track | Clickhouse |
| Team size | 1 |
| Open-source repository | https://github.com/ezrawestover1-hub/slateguard-agentic-cinema |
| Hosted project | https://sprint2---slateguard-vseh3ye7mq-uc.a.run.app |
| Google Cloud products | Google Cloud Run for the public FastAPI + React service; Vertex AI and Google ADK / Agent Runtime for Gemini structured Change Packets; Artifact Registry and Cloud Build for container build/deploy; Secret Manager for runtime secret delivery; Cloud Logging for redacted operational traces. |
| Other tools/products | ClickHouse Cloud as the production-memory store; official Python `mcp-clickhouse` for separate reader/writer MCP paths; React, TypeScript, Vite, Python, FastAPI, Docker, and GitHub. |
| First time using IBM | N/A, I am not submitting for the IBM track. |
| First time using Grafana | N/A, I'm not submitting for the Grafana track. |
| First time using Parallel | N/A, I am not submitting to the Parallel track. |
| First time using ClickHouse | **Confirm before submit** |
| First time using Replit | N/A, I am not submitting to the Replit track. |

## Final pre-submit gate

- [x] Open Cloud Run demo URL
- [x] Public GitHub repository with MIT license
- [x] Required Clickhouse track selected in this draft
- [x] Judge-focused description, proof map, and captions prepared
- [ ] Mix natural narration into the 2:20 cut and upload it publicly to YouTube or Vimeo
- [ ] Paste the public video URL into this file and Devpost
- [ ] Confirm government-employment, country, and first-time-ClickHouse answers
- [ ] Upload the five current product screenshots (not obsolete design references)
- [ ] Run one fresh-browser rehearsal from reset through the verified receipt

## Known limitations

SlateGuard is intentionally a focused demo slice rather than a full production-management platform. It supports one self-authored fictional revision scenario, has no external project-management notification integration, and does not contain real production data. The restricted scenario is deliberate: it makes the authority boundary and ClickHouse proof inspectable end-to-end.
