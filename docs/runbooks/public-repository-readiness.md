# Public Repository Readiness

Use this checklist immediately before creating or pushing a public repository for SlateGuard. It is a publication guardrail, not an instruction to publish automatically.

## Current Readiness Snapshot — 2026-08-18

- [x] MIT license is present.
- [x] README explains the product, trust boundary, architecture, local run path, and live demo link.
- [x] `.gitignore` excludes local environment files, credential JSON files, Python environments, build output, and recordings.
- [x] Read-only filename and heuristic source scan found no candidate private key, provider key, ClickHouse URI with embedded password, or credential file in the publish candidate. Local `.env` remains ignored; `.devpost-hackathon-state.json` and generated TypeScript build metadata are also ignored.
- [ ] A public remote repository has not been created.
- [x] The current official Gitleaks release scanned the exact `git ls-files --others --exclude-standard` publish candidate on 2026-08-18 with zero findings. A broader workspace scan found redacted matches only in ignored local `.env` and generated video-build artifacts.
- [ ] The deployed Impact Pulse, decision-receipt screenshots, and a 180-second 1920×1080 H.264 proof cut are ready locally; its final public upload is still required for the Devpost draft.

## Pre-Publish Gate

1. Run a full secret scan before the first public push. Inspect any result by file and line; revoke and replace a real credential before publishing.
2. Confirm `git status --short` contains no `.env`, service-account JSON, recording, or local-data artifact.
3. Review `.env.example` to ensure it contains variable names and comments only.
4. Run the backend unit suite and frontend production build.
5. Open the public Cloud Run URL from a clean browser and complete the supported revision flow.
6. Review the README and `devpost-submission.md` for claims that still match the current product.
7. Create a public repository only after the preceding checks pass; add its URL to `devpost-submission.md`.

## What Belongs in the Public Repository

- Application source, tests, ClickHouse schema and curated-view definitions, frontend, infrastructure templates, runbooks, and the MIT license.
- Self-authored fictional production fixtures only.
- A blank `.env.example` with variable names and safe comments.

## What Must Never Be Published

- `.env` or environment-specific configuration containing values.
- ClickHouse passwords, Google tokens, service-account private keys, OAuth codes, or Secret Manager payloads.
- Full production endpoints, connection strings, browser recording profiles, or user data.
- Any footage, script, or production data that is not cleared for public release.

## Recommended First Public Commit Scope

The repository is currently an uncommitted local worktree. Make the first commit represent the reviewed release candidate: source, tests, documentation, schema, and configuration templates only. Keep the public-live runtime configuration in Google Cloud Secret Manager, not in Git.
