# Sprint 0 Google ADK runbook

This runbook proves that SlateGuard can use the permitted Google agent path before user-interface work begins. The first proof is intentionally a no-tools, schema-constrained extraction request. The ClickHouse MCP proof is separate because ADK documents limitations when output schemas and tools are combined.

## 1. Human-owned cloud setup

Create or select an isolated Google Cloud project and attach the confirmed credit. Use us-central1 for Agent Runtime deployment and create a same-region staging bucket when preparing the remote proof.

Enable these APIs:

```text
aiplatform.googleapis.com
cloudresourcemanager.googleapis.com
storage.googleapis.com
logging.googleapis.com
monitoring.googleapis.com
telemetry.googleapis.com
cloudtrace.googleapis.com
```

The local deployer needs Vertex AI User and Service Usage Consumer access. Only grant Service Usage Admin if the deployer must enable APIs. The remote agent uses the Agent Runtime agent identity; later, give that identity Secret Manager access only after secrets are introduced.

## 2. Local authentication

Use Application Default Credentials, not an API key or service-account JSON file:

```sh
gcloud auth login
gcloud auth application-default login
gcloud auth application-default set-quota-project "$GOOGLE_CLOUD_PROJECT"
```

Copy .env.example to .env locally and set:

```text
GOOGLE_GENAI_USE_ENTERPRISE=TRUE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_GENAI_LOCATION=us-central1
SG_AGENT_RUNTIME_LOCATION=us-central1
```

## 3. Local proof

```sh
.venv/bin/python -m pip install -r requirements-sprint0.txt
set -a
source .env
set +a
.venv/bin/python probes/google_adk_probe.py
```

Expected result: a local-adk record containing a schema-validated FactChange for Scene 12's blue-jacket to black-jacket revision.

## 4. Managed Agent Runtime proof

Create a uniformly-accessible us-central1 staging bucket, set SG_GCP_STAGING_BUCKET to its gs:// URL, then opt in to creation of the billable managed resource:

```sh
export SG_DEPLOY=1
.venv/bin/python probes/google_adk_probe.py
```

Expected result: an Agent Runtime reasoningEngines resource name followed by a separately validated deployed-agent-runtime response. Do not set GOOGLE_CLOUD_LOCATION in the deployed Agent Runtime environment; that location is controlled by the runtime deployment.

## 5. Evidence to retain

Record the exact installed dependency versions, region, model, project ID, Agent Runtime resource name, timestamp, and validation result in docs/sprint-0.md. Never commit credential files or copy access tokens into issue text, video, or documentation.
