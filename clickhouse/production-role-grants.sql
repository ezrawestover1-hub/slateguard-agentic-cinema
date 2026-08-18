-- Run once in the ClickHouse Cloud SQL console as the service admin,
-- after clickhouse/schema.sql. These grants preserve the runtime boundary:
-- reader = curated views only; writer = append-only event tables only.

GRANT SELECT ON mart.sg_scene_evidence TO sg_mcp_read_role;
GRANT SELECT ON mart.sg_scheduled_dependencies TO sg_mcp_read_role;
GRANT SELECT ON mart.sg_actionable_revisions TO sg_mcp_read_role;
GRANT SELECT ON mart.sg_followup_receipts TO sg_mcp_read_role;

GRANT INSERT ON core.revision_events TO sg_mcp_write_role;
GRANT INSERT ON core.impact_snapshots TO sg_mcp_write_role;
GRANT INSERT ON core.followup_action_events TO sg_mcp_write_role;
GRANT INSERT ON core.readiness_events TO sg_mcp_write_role;

-- Validate every grant individually in the SQL console before running the app.
SHOW GRANTS FOR sg_mcp_read_role;
SHOW GRANTS FOR sg_mcp_write_role;
