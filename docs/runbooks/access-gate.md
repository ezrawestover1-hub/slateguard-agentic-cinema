# SlateGuard Access Gate

This is the only setup step that creates cloud resources or can consume the Google Cloud credit. Complete it in the browser while signed into the intended Google account. Do not paste passwords, API keys, tokens, connection strings, or screenshots containing them into Codex, Git, or this repository.

## Approved resource shape

| Resource | Exact choice | Reason |
| --- | --- | --- |
| Google Cloud project | New isolated project named `SlateGuard Agentic Cinema 2026`; choose a unique project ID at creation. | Separates hackathon spend, IAM, logs, and cleanup from other work. |
| GCP region | `us-central1` | Matches the selected Gemini 2.5 Flash / Agent Runtime deployment plan. |
| Billing guardrail | Attach the approved credit/billing account; create a **$300 USD** budget alert at 50%, 80%, and 100%. | Preserves at least $150 of the stated credit for rehearsal/recovery. Alerts do not cap spending, so avoid non-required services. |
| Google services | Vertex AI, Cloud Run, Artifact Registry, Secret Manager, Cloud Storage, Cloud Logging, Cloud Monitoring. | The smallest managed set required by the architecture. |
| ClickHouse Cloud | One small real service, preferably on GCP in `us-central1` or the nearest available US region; database name `slateguard_demo`. | Enables real TLS runtime proof while keeping latency and service surface small. |
| ClickHouse identities | `sg_mcp_read` (curated `SELECT` only) and `sg_mcp_write` (named event-table `INSERT` only); create a separate admin identity for setup. | Keeps the agent/browser unable to write production-memory records. |

## Browser sequence

1. In Google Cloud Console, create the isolated project. Attach the approved billing/credit account only after confirming the account is the intended one.
2. Create the $300 budget alert and choose the owner’s preferred notification address in the console. Do not record the email address in this repository.
3. Enable only these APIs: `aiplatform.googleapis.com`, `run.googleapis.com`, `artifactregistry.googleapis.com`, `secretmanager.googleapis.com`, `storage.googleapis.com`, `logging.googleapis.com`, `monitoring.googleapis.com`, `cloudresourcemanager.googleapis.com`, `serviceusage.googleapis.com`, `telemetry.googleapis.com`, and `cloudtrace.googleapis.com`.
4. Create a small, region-aligned ClickHouse Cloud service and the `slateguard_demo` database. Do not turn on a managed Remote MCP service: SlateGuard needs controlled write proof through the official `mcp-clickhouse` Python server.
5. In the ClickHouse SQL console, follow [Sprint 0 ClickHouse MCP runbook](../sprint-0-clickhouse-runbook.md) to create the smoke table and two least-privilege roles/users. Use strong unique passwords generated and retained by your password manager.
6. Add each ClickHouse credential separately to Secret Manager. Use names such as `slateguard-ch-reader-password` and `slateguard-ch-writer-password`; keep the hostname/database as non-secret runtime configuration only if desired.
7. Give the eventual Cloud Run service identity access only to the specific secrets it needs. Do not grant browser users, the ADK agent, or a broad default service account writer access.

## Safe handoff back to Codex

When the browser work is complete, create a local ignored `.env` from `.env.example` and fill only the variables requested by the two Sprint 0 runbooks. Do not send their values in chat.

Then tell Codex only these non-secret facts:

```text
GCP project created: yes
Billing/credit attached and $300 alert set: yes
ClickHouse service created: yes
Reader/writer users created: yes
.env filled locally: yes
```

Codex will then run the safe real-runtime probes, redact the evidence, and continue automatically.
