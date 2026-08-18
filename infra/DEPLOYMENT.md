# SlateGuard deployment boundary

The container is intentionally deployable before external services are available, but it is not a usable product until the runtime bootstrap injects real services. Before any public deployment, confirm all of the following:

1. The official ClickHouse MCP reader/write/read proof passed against the Cloud service.
2. The schema and fictional seed were applied and reader-verified.
3. The deployed Google Agent Runtime produced a schema-valid Change Packet.
4. A dedicated Cloud Run service account can read only `slateguard-demo-session-secret`, `slateguard-ch-reader-password`, and `slateguard-ch-writer-password` in Secret Manager.
5. `SLATEGUARD_DEMO_SESSION_SECRET`, reader credentials, writer credentials, ClickHouse host/database/usernames, and `SG_CHANGE_PACKET_RUNTIME_RESOURCE` are provided outside source control.

Cloud Run must remain fail-closed until the real service bootstrap is connected. Do not deploy a fixture or test-double configuration as the public demo.
