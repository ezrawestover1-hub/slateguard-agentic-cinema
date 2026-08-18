-- SlateGuard's public demo database. All runtime state is append-only.
CREATE DATABASE IF NOT EXISTS core;
CREATE DATABASE IF NOT EXISTS mart;

CREATE TABLE IF NOT EXISTS core.scenes (
  scene_id String,
  scene_number UInt16,
  title String,
  shoot_status LowCardinality(String),
  shoot_date Date,
  created_at DateTime64(3, 'UTC')
) ENGINE = MergeTree ORDER BY scene_id;

CREATE TABLE IF NOT EXISTS core.scene_fact_versions (
  fact_id UUID,
  scene_id String,
  fact_type LowCardinality(String),
  value String,
  valid_from DateTime64(3, 'UTC'),
  source_id String,
  created_at DateTime64(3, 'UTC')
) ENGINE = MergeTree ORDER BY (scene_id, fact_type, valid_from, fact_id);

CREATE TABLE IF NOT EXISTS core.source_evidence (
  evidence_id String,
  scene_id String,
  kind LowCardinality(String),
  wardrobe_value Nullable(String),
  shoot_status Nullable(String),
  excerpt String,
  occurred_at DateTime64(3, 'UTC')
) ENGINE = MergeTree ORDER BY (scene_id, kind, occurred_at, evidence_id);

CREATE TABLE IF NOT EXISTS core.scene_dependencies (
  dependency_id String,
  source_scene_id String,
  target_scene_id String,
  dependency_type LowCardinality(String),
  shoot_date Date,
  status LowCardinality(String),
  evidence_id String
) ENGINE = MergeTree ORDER BY (source_scene_id, target_scene_id, dependency_id);

CREATE TABLE IF NOT EXISTS core.revision_events (
  demo_session_id UUID,
  revision_id UUID,
  scene_id String,
  fact_type LowCardinality(String),
  old_value String,
  new_value String,
  idempotency_key String,
  recorded_at DateTime64(3, 'UTC')
) ENGINE = MergeTree ORDER BY (demo_session_id, revision_id, recorded_at);

CREATE TABLE IF NOT EXISTS core.impact_snapshots (
  demo_session_id UUID,
  packet_id UUID,
  revision_id UUID,
  impact_type LowCardinality(String),
  evidence_ids Array(String),
  affected_scene_ids Array(String),
  rule_version String,
  recorded_at DateTime64(3, 'UTC')
) ENGINE = MergeTree ORDER BY (demo_session_id, revision_id, packet_id, recorded_at);

CREATE TABLE IF NOT EXISTS core.followup_action_events (
  demo_session_id UUID,
  action_id UUID,
  revision_id UUID,
  owners Array(String),
  status LowCardinality(String),
  created_at DateTime64(3, 'UTC')
) ENGINE = MergeTree ORDER BY (demo_session_id, revision_id, action_id, created_at);

CREATE TABLE IF NOT EXISTS core.readiness_events (
  demo_session_id UUID,
  readiness_event_id UUID,
  revision_id UUID,
  state LowCardinality(String),
  reason String,
  recorded_at DateTime64(3, 'UTC')
) ENGINE = MergeTree ORDER BY (demo_session_id, revision_id, recorded_at);

-- SECURITY DEFINER keeps the reader identity constrained to these curated
-- projections; it does not need SELECT on the underlying core tables.
CREATE VIEW IF NOT EXISTS mart.sg_scene_evidence
DEFINER = CURRENT_USER SQL SECURITY DEFINER AS
SELECT evidence_id, scene_id, kind, wardrobe_value, shoot_status, excerpt, occurred_at
FROM core.source_evidence;

CREATE VIEW IF NOT EXISTS mart.sg_scheduled_dependencies
DEFINER = CURRENT_USER SQL SECURITY DEFINER AS
SELECT dependency_id, source_scene_id, target_scene_id, shoot_date, status, evidence_id
FROM core.scene_dependencies
WHERE status = 'scheduled';

CREATE VIEW IF NOT EXISTS mart.sg_actionable_revisions
DEFINER = CURRENT_USER SQL SECURITY DEFINER AS
SELECT demo_session_id, revision_id
FROM core.revision_events;

CREATE VIEW IF NOT EXISTS mart.sg_followup_receipts
DEFINER = CURRENT_USER SQL SECURITY DEFINER AS
SELECT
  followup.demo_session_id,
  followup.action_id,
  followup.revision_id,
  followup.owners,
  followup.status,
  argMax(readiness.state, readiness.recorded_at) AS readiness_state
FROM core.followup_action_events AS followup
INNER JOIN core.readiness_events AS readiness
  ON followup.demo_session_id = readiness.demo_session_id
  AND followup.revision_id = readiness.revision_id
GROUP BY
  followup.demo_session_id,
  followup.action_id,
  followup.revision_id,
  followup.owners,
  followup.status;
