# SlateGuard contest lock

This file is the implementation-time guardrail for SlateGuard's Agentic Cinema ClickHouse-track submission. The live Devpost rules control if anything here conflicts with them.

## Target

- Event: Agentic Cinema: The Blockbuster Hackathon
- Partner track: ClickHouse
- Submission deadline: Sept. 7, 2026, 2:00 PM PT
- Internal target: feature freeze Sept. 5; submit Sept. 6

## Required runtime

- Gemini and Google Cloud Agent Builder / Gemini Enterprise Agent Platform
- A functional web, Android, or iOS application; SlateGuard is a web application
- Official mcp-clickhouse server at runtime against a real ClickHouse Cloud or self-hosted cluster
- Actual Google Cloud and ClickHouse calls in the main user path, visible in source and demo evidence

## Prohibited or intentionally excluded

- No non-Google AI models, agent frameworks, or AI APIs
- No mock ClickHouse result on the primary demo path
- No generic chatbot-first interface
- No autonomous production decision or write by the model
- No authentication, collaboration, notification, video-analysis, vector-search, or second-database scope

## Required proof chain

Revision
→ official ClickHouse MCP query and validated write
→ source evidence and deterministic impact checks
→ Gemini-grounded Change Packet
→ human-created follow-up
→ persisted readiness update

## Submission readiness

- Public hosted application
- Public source repository with a detectable OSI-approved license and runnable instructions
- Public functional demo video of no more than three minutes, in English or with English subtitles
- Original, rights-cleared fictional production data and assets only
- Accurate Devpost form, including ClickHouse track and all technology disclosures

## Change-control rule

Do not add a feature unless it makes the required proof chain more real, more visible, or more reliable.
