# SlateGuard Judge Cut — Narration and Recording Plan

`SlateGuardJudgeCut` is the polished, 2-minute-20-second, caption-led submission cut. It shows the actual live workspace as well as the runtime proof, then makes the ClickHouse role and human ownership boundary explicit. It is intentionally muted, so a natural human voiceover can be recorded later without needing to rebuild the visual edit.

| Time | Voiceover |
| --- | --- |
| 0:00–0:10 | “Production changes rarely stay isolated. SlateGuard turns a creative change into a current, grounded decision.” |
| 0:10–0:30 | “Scene 12 changes from a blue jacket to black. Scene 11 has already been captured, and Scenes 13 and 14 are scheduled next. Before anyone acts, SlateGuard shows cited evidence, the affected scenes, risk, and named owners.” |
| 0:30–0:50 | “This is the live review workspace. The change queue scopes the request. The decision brief keeps cited evidence visible. Risk, affected scenes, and human owners stay beside the action.” |
| 0:50–1:10 | “The ClickHouse reader MCP retrieves only the relevant production window: prior continuity, the revision, and next scheduled dependencies. Archive, unrelated, and unscheduled work are excluded before Gemini explains impact.” |
| 1:10–1:30 | “A separate append-only writer records the revision. The reader returns curated evidence. The Change Packet is grounded in those facts. Gemini explains the evidence; it does not run SQL or create the consequential task.” |
| 1:30–1:50 | “A human owner reviews the cited impact and creates the follow-up for Wardrobe and the Assistant Director. SlateGuard reads the receipt through the safe path and confirms readiness changed from At risk to Follow-up created.” |
| 1:50–2:10 | “That is why ClickHouse is not background storage. It is the time-aware memory the agent must consult for current context. Its curated views keep irrelevant history out and give the agent a fast, governed evidence path.” |
| 2:10–2:20 | “Current context. Grounded decision. Human action. That’s SlateGuard.” |

## Recording Direction

- Record a single, steady take in a quiet room; speak slightly slower than the on-screen captions and leave a short breath at each scene boundary.
- Use the exact timing above. The captions stay visible even when the narration is muted, so judges can follow the whole argument without sound.
- If replacing the capture sequence with a live browser recording later, begin on a fresh SlateGuard demo session, apply the revision once, wait for all three trace states, and create the follow-up once.
- Keep browser chrome, notifications, raw Cloud Console screens, credentials, and SQL out of the frame.
