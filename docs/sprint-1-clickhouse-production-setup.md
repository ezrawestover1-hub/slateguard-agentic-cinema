# Sprint 1 — ClickHouse production-memory setup

The Sprint 0 smoke proof is complete. This separate, one-time admin setup makes the real SlateGuard tables available to the restricted runtime identities without broadening them to the underlying production tables.

## Completed production setup — 2026-08-17

- The `core` and `mart` schemas, append-only event tables, and security-definer curated views are live.
- The self-authored six-scene seed was already present, so it was retained without duplication.
- The two reader-view and four writer-table grants were applied sequentially in the SQL console.
- The actual SlateGuard MCP runner passed the four-evidence/two-dependency read path and writer append; the cross-role denial checks also passed.
- The `mart.sg_actionable_revisions` and `mart.sg_followup_receipts` security-definer views are live. The reader role has `SELECT` on those views only; it received no direct `core`-table permission.
- A real, session-scoped Scene 12 revision passed actionability verification, persisted the Wardrobe + Assistant Director follow-up and readiness transition, then returned a reader-confirmed receipt with the prior-dailies and both call-sheet evidence IDs.

## Reference procedure

1. Open the service's SQL console as its admin user.
2. Run [schema.sql](../clickhouse/schema.sql), then [seed.sql](../clickhouse/seed.sql), then [production-role-grants.sql](../clickhouse/production-role-grants.sql), in that order.
3. Run these two read-only validation queries as `sg_mcp_read` through the app adapter:

```sql
SELECT evidence_id, scene_id, kind, wardrobe_value, shoot_status, excerpt
FROM mart.sg_scene_evidence
WHERE scene_id IN ('scene-11', 'scene-12', 'scene-13', 'scene-14')
ORDER BY occurred_at ASC;

SELECT dependency_id, source_scene_id, target_scene_id, shoot_date, status, evidence_id
FROM mart.sg_scheduled_dependencies
WHERE source_scene_id = 'scene-12'
ORDER BY target_scene_id ASC;
```

The views are explicitly `SQL SECURITY DEFINER`. ClickHouse normally evaluates a view with the invoker's underlying-table permissions; defining these views lets `sg_mcp_read` select only their approved columns and rows rather than receive `SELECT` on `core` tables. This is the intentional least-privilege boundary.

## Required proof

- Reader can retrieve four evidence records and two scheduled dependencies through the official MCP process.
- Reader cannot `INSERT` into any `core` event table.
- Writer can append a typed revision event, but cannot select either curated view.
- `SHOW GRANTS` shows only the named grants in `production-role-grants.sql` plus the existing smoke-test grants.

Do not add an admin credential to `.env`, Cloud Run, Agent Runtime, the browser, a demo recording, or source control.
