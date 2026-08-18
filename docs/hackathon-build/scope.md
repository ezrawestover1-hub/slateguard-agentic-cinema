# Project Scope

## Project Name Candidates

- SlateGuard (selected)
- Production Change Packet
- Continuity Command Desk

## One-Line Summary

SlateGuard turns one scripted production revision into a ClickHouse-backed evidence packet, a human-owned follow-up, and an updated shoot-readiness state.

## Target User

A script supervisor reviewing a creative change before it creates a continuity or next-shoot problem.

## Problem

Production revisions are commonly passed through prose, spreadsheets, and informal messages. Teams can miss footage already shot, future call-sheet dependencies, or the decision history behind an intentional variation. The result is avoidable rework and unclear ownership.

## Core Workflow

1. Load a synthetic six-scene production.
2. Change Scene 12 wardrobe from blue jacket to black jacket.
3. Persist the validated revision through the official ClickHouse MCP writer path.
4. Retrieve source evidence through the separate read-only official ClickHouse MCP path.
5. Run deterministic continuity and schedule-dependency checks.
6. Present a grounded Gemini Change Packet with evidence and a bounded recommendation.
7. The script supervisor creates one follow-up; SlateGuard persists and verifies the resulting readiness event.

## What We Are Building

- A public web app with a single premium **Continuity Command Desk** workflow.
- A self-authored, resettable six-scene production dataset, plus 15–20 labeled change fixtures.
- A real ClickHouse service reached at runtime through the official `mcp-clickhouse` server, using separate reader and writer identities.
- Gemini on Google Cloud Agent Builder / ADK for structured fact extraction and evidence-grounded explanation.
- Deterministic checks for one continuity conflict and one already-shot/scheduled downstream dependency.
- A visible Live Evidence Trace: revision persisted, MCP evidence retrieved, rule triggered, follow-up persisted, readiness refreshed.
- A human-only `Create follow-up` decision and append-only decision/readiness history.
- Black/near-black ClickHouse-adjacent information architecture; high-signal green for product actions and confirmed status; ClickHouse yellow reserved for MCP/query evidence events; off-white only for source excerpts.

## What We Are Not Building

- Generic chat, open-ended agent behavior, or model-written SQL.
- Authentication, collaboration, notifications, calendars, budget management, or full studio operations.
- Video upload/analysis, computer vision, media generation, or copyrighted source material.
- Multiple partner tracks, extra databases, vector search, queues, an ORM, or multiple agents without a critical role.
- Autonomous production decisions or writes exposed to the model.

## Inspiration And References

- **ClickHouse:** the product interaction should feel query/evidence-forward, fast, data-dense, and technically legible.
- **GitHub pull requests:** visible change, inspectable context, and a deliberate human decision.
- **Kalshi:** color confidence only—near-black shell and decisive green states—not product interaction or trading metaphors.

## Demo Path

In under 30 seconds, the judge changes the jacket color and sees the live trace complete: immutable revision write, ClickHouse evidence retrieval, Scene 11 already-shot conflict, two scheduled dependent scenes, a grounded Change Packet, and a human-created follow-up that updates readiness. The rest of the video proves the integration is real, shows the source records, and closes with the decision audit trail.

## Submission Story

SlateGuard is not a film-industry chatbot. It is a production-change intelligence system: ClickHouse serves as time-aware production memory, Google ADK interprets retrieved evidence, deterministic rules make the risk legible, and a human owns the consequential decision. The project will target the ClickHouse track and prove each part in the public app, repository, and functional demo video.

## Scope Rationale And Time Budget

The participant has 120+ focused hours before the Sept. 5 feature freeze and reports fast recent shipping. The core scope remains deliberately narrow and should take roughly 70 focused hours. The remaining capacity is reserved for runtime proof, fixture evaluation, reliability, visual refinement, public deployment, recording rehearsal, and submission quality—not broader features.
