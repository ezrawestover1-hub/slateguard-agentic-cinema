# Sprint 0 ClickHouse MCP runbook

This runbook proves the real ClickHouse requirement before product work begins. It uses the official mcp-clickhouse package at version 0.4.1, Python 3.12, ClickHouse Cloud HTTPS on port 8443, and two least-privilege identities.

## 1. Human-owned cloud setup

In ClickHouse Cloud, create a small service and copy only the Connect-panel hostname. Do not put credentials in the repository, terminal history, screenshots, or video.

Run the following as the ClickHouse admin, replacing the two password placeholders in the Cloud console only:

```sql
CREATE DATABASE IF NOT EXISTS slateguard_spike;

CREATE TABLE IF NOT EXISTS slateguard_spike.mcp_smoke_events
(
  event_id UUID,
  event_kind LowCardinality(String),
  actor LowCardinality(String),
  created_at DateTime64(3, 'UTC')
)
ENGINE = MergeTree
ORDER BY (created_at, event_id);

CREATE ROLE IF NOT EXISTS sg_mcp_read_role;
GRANT SELECT ON slateguard_spike.mcp_smoke_events TO sg_mcp_read_role;
GRANT SELECT ON system.settings TO sg_mcp_read_role;
ALTER ROLE sg_mcp_read_role SETTINGS
  readonly = 1,
  max_execution_time = 15,
  max_rows_to_read = 10000,
  max_bytes_to_read = 10000000,
  max_threads = 2;

CREATE ROLE IF NOT EXISTS sg_mcp_write_role;
GRANT INSERT ON slateguard_spike.mcp_smoke_events TO sg_mcp_write_role;
GRANT SELECT ON system.settings TO sg_mcp_write_role;
ALTER ROLE sg_mcp_write_role SETTINGS
  max_execution_time = 15,
  max_threads = 2;

CREATE USER IF NOT EXISTS sg_mcp_read
  IDENTIFIED WITH sha256_password BY '<READER_PASSWORD>';
GRANT sg_mcp_read_role TO sg_mcp_read;
ALTER USER sg_mcp_read DEFAULT ROLE sg_mcp_read_role;

CREATE USER IF NOT EXISTS sg_mcp_write
  IDENTIFIED WITH sha256_password BY '<WRITER_PASSWORD>';
GRANT sg_mcp_write_role TO sg_mcp_write;
ALTER USER sg_mcp_write DEFAULT ROLE sg_mcp_write_role;
```

Set CLICKHOUSE_DATABASE=slateguard_spike while running this smoke test. The production schema comes later.

## 2. Local configuration

Copy .env.example to .env locally, then populate the host and two credentials. Use:

```text
CLICKHOUSE_PORT=8443
CLICKHOUSE_SECURE=true
CLICKHOUSE_VERIFY=true
CLICKHOUSE_DATABASE=slateguard_spike
```

Install the locked Sprint 0 dependencies using the bundled Python 3.12:

```sh
.venv/bin/python -m pip install -r requirements-sprint0.txt
.venv/bin/python -m pip check
```

## 3. Proof command

```sh
set -a
source .env
set +a
.venv/bin/python probes/clickhouse_mcp_probe.py --mode all
```

Expected result: one reader query, one writer INSERT, one reader verification, and two denied negative checks. The script has no arbitrary-query flag by design; it proves that the server-side path is safe before a model can use it.

## 4. Evidence to retain

Record the mcp-clickhouse version, non-secret hostname suffix, reader/writer PASS results, and timestamp in docs/sprint-0.md. Do not record passwords, connection strings, or raw query output containing secrets.
