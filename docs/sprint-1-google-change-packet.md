# Sprint 1 — Google Change Packet agent

SlateGuard separates deterministic authority from Gemini narration. The backend first writes and reads through named, least-privilege ClickHouse MCP templates, evaluates the continuity and schedule rules itself, then sends the agent only a bounded packet: supplied evidence IDs, deterministic findings, readiness, and follow-up eligibility.

## Live proof — 2026-08-17

- Runtime resource: `projects/136906134633/locations/us-central1/reasoningEngines/4527341931704877056`
- Model and region: `gemini-2.5-flash` in `us-central1`
- Deployment probe: [change_packet_agent_probe.py](../probes/change_packet_agent_probe.py)
- Verified output: `ready`; only the three supplied evidence IDs; only Wardrobe and Assistant Director; `distinguishes_unknowns: true`.

The probe rejects any output that adds evidence, downgrades an actionable packet to review, suggests another owner, or fails to distinguish known evidence from unknowns. It contains neither ClickHouse credentials nor any write tool.

## Next integration gate

The public API must read `SG_CHANGE_PACKET_RUNTIME_RESOURCE` as non-secret configuration, invoke the managed runtime through the existing `GoogleChangePacketGateway`, validate its result with the existing bounded contract, and visibly mark deterministic fallback only when that real call fails.
