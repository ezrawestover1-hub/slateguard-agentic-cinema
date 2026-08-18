import { useEffect, useMemo, useState } from "react";
import { api, ImpactPulse, ReceiptResponse, RevisionResponse, RuntimeStatus } from "./api";

type RuntimeState = "loading" | RuntimeStatus | "unavailable";

const baselineEvidence = [
  { id: "ev-dailies-11-blue", label: "Scene 11 dailies", detail: "Already captured · blue jacket", kind: "Continuity" },
  { id: "ev-call-sheet-13", label: "Scene 13 call sheet", detail: "Scheduled next · wardrobe dependent", kind: "Schedule" },
  { id: "ev-call-sheet-14", label: "Scene 14 call sheet", detail: "Scheduled next · wardrobe dependent", kind: "Schedule" },
];

const traceLabels: Record<string, { title: string; idle: string }> = {
  writer_mcp: { title: "Writer MCP", idle: "Revision event awaits the protected writer path." },
  reader_mcp: { title: "Reader MCP", idle: "Curated evidence returns through the reader path." },
  change_packet_agent: { title: "Change Packet agent", idle: "Grounded packet awaits agent validation." },
};

function EvidenceIcon({ kind }: { kind: string }) {
  return <span className={`evidence-icon ${kind === "Schedule" ? "calendar" : "film"}`} aria-hidden="true">{kind === "Schedule" ? "□" : "▣"}</span>;
}

function CheckIcon() {
  return <span className="check-icon" aria-hidden="true">✓</span>;
}

export function App() {
  const [runtime, setRuntime] = useState<RuntimeState>("loading");
  const [pulse, setPulse] = useState<ImpactPulse | null>(null);
  const [revision, setRevision] = useState<RevisionResponse | null>(null);
  const [receipt, setReceipt] = useState<ReceiptResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.runtime().then((body) => setRuntime(body.state)).catch(() => setRuntime("unavailable"));
    api.impactPulse().then(setPulse).catch(() => setPulse(null));
  }, []);

  const actionReady = runtime === "ready";
  const runtimeLabel = actionReady ? "Verified" : runtime === "loading" ? "Checking runtime" : "Runtime unavailable";
  const citedIds = revision?.packet.cited_evidence_ids ?? baselineEvidence.map((item) => item.id);
  const sourceEvidence = useMemo(() => baselineEvidence.filter((item) => citedIds.includes(item.id)), [citedIds]);
  const trace = revision?.trace ?? [];
  const receiptTrace = receipt?.trace ?? [];
  const traceSteps = ["writer_mcp", "reader_mcp", "change_packet_agent"];

  async function applyRevision() {
    setBusy(true); setError(null); setReceipt(null);
    try { await api.reset(); setRevision(await api.revise(crypto.randomUUID())); }
    catch (cause) { setError(cause instanceof Error ? cause.message : "Unable to analyze revision."); }
    finally { setBusy(false); }
  }

  async function createFollowup() {
    if (!revision) return;
    setBusy(true); setError(null);
    try { setReceipt(await api.followup(revision.revision_id, crypto.randomUUID())); }
    catch (cause) { setError(cause instanceof Error ? cause.message : "Unable to create follow-up."); }
    finally { setBusy(false); }
  }

  const currentReadiness = receipt?.readiness_to ?? revision?.evaluation.readiness ?? "At risk";
  const currentOwners = receipt?.owners ?? revision?.packet.recommended_owners ?? ["Wardrobe", "Assistant Director"];

  return <main className="desk-shell">
    <header className="topbar">
      <a className="brand" href="#desk" aria-label="SlateGuard Command Desk">SLATE<span>GUARD</span></a>
      <span className="topbar-divider" aria-hidden="true" />
      <p>Production change control</p>
      <div className={`runtime ${actionReady ? "connected" : ""}`}><CheckIcon />{runtimeLabel}</div>
    </header>
    <section className="workspace" id="desk" aria-label="Scene 12 command desk">
      <aside className="scene-panel">
        <div className="panel-intro"><h1>Scene 12</h1><p>Revision context</p></div>
        <div className="context-group"><span className="field-label">Change</span><div className="change-line"><strong>Blue jacket</strong><span className="change-arrow" aria-hidden="true">→</span><strong>Black jacket</strong></div></div>
        <div className="context-group"><span className="field-label">Status</span><div className={`status-line ${receipt ? "resolved" : ""}`}><span className="status-icon" aria-hidden="true">△</span>{currentReadiness}</div></div>
        <div className="context-group"><span className="field-label">Source of change</span><p>Continuity from Scene 11</p></div>
        <div className="context-group context-description"><span className="field-label">Description</span><p>Wardrobe continuity correction to match footage already established in Scene 11.</p></div>
        <div className="context-group owner-group"><span className="field-label">Owners</span>{currentOwners.map((owner) => <div className="owner-row" key={owner}><span className="owner-mark" aria-hidden="true">{owner === "Wardrobe" ? "⌁" : "▤"}</span><span>{owner}</span><span className="row-arrow" aria-hidden="true">›</span></div>)}</div>
        <div className="context-group updated"><span className="field-label">Live state</span><p>{receipt ? "Follow-up receipt verified" : revision ? "Evidence packet ready" : "Ready for a controlled revision"}</p></div>
      </aside>
      <section className="packet-panel" aria-live="polite">
        <div className="packet-heading"><h2>Change Packet</h2><p>Evidence-first. Grounded. Measurable impact.</p></div>
        <section className="relevance-pulse" aria-label="ClickHouse relevance scope">
          <div className="pulse-intro"><span className="field-label">Live Impact Pulse</span><strong>{pulse ? "Reader MCP · active production window" : "Reader MCP · scope loading"}</strong><p>{pulse?.scope ?? "Scene 11 history · Scene 12 revision · next scheduled dependencies"}</p></div>
          <div><span className="field-label">Evidence surfaced</span><strong>{pulse?.relevant_evidence_records ?? "—"}</strong></div>
          <div><span className="field-label">Affected scenes</span><strong>{pulse?.affected_scenes ?? "—"}</strong></div>
          <p className="scope-policy"><CheckIcon />Archive, unrelated, and unscheduled work excluded by policy.</p>
        </section>
        <div className="content-section"><span className="field-label">Evidence</span><div className="evidence-table" role="table" aria-label="Cited source evidence"><div className="evidence-head" role="row"><span>Type</span><span>Source</span><span>Details</span><span>State</span></div>{sourceEvidence.map((item) => <article className="evidence-row" key={item.id} role="row"><span className="type-cell"><EvidenceIcon kind={item.kind} />{item.kind}</span><strong>{item.label}</strong><span>{item.detail}</span><span className="verified-cell"><CheckIcon />Cited</span></article>)}</div></div>
        <div className="content-section"><span className="field-label">Impact</span><div className="impact-list"><article><span className="impact-number">01</span><div><strong>Continuity conflict</strong><p>Scene 11 footage establishes the prior wardrobe state.</p></div><span>Scene 11–12</span></article><article><span className="impact-number">02</span><div><strong>Schedule dependency</strong><p>Connected call sheets need coordinated wardrobe review.</p></div><span>Scenes 13–14</span></article></div></div>
        <div className="packet-summary"><div><span className="field-label">Change</span><p>Blue jacket <span>→</span> Black jacket</p></div><div><span className="field-label">Owners</span><p>{currentOwners.length}</p></div><div><span className="field-label">Affected scenes</span><p>{pulse?.affected_scenes ?? 2}</p></div><div><span className="field-label">Readiness</span><p className={receipt ? "resolved-text" : "risk-text"}>{currentReadiness}</p></div></div>
      </section>
      <aside className="trace-panel">
        <div className="panel-intro"><h2>Trace</h2><p>Auditable change trail</p></div>
        <ol className="trace-list">{traceSteps.map((step, index) => {
          const traceEntry = trace.find((entry) => entry.step === step) ?? receiptTrace.find((entry) => entry.step === step);
          const metadata = traceLabels[step];
          return <li className={traceEntry ? "confirmed" : ""} key={step}><div className="trace-marker">{traceEntry ? <CheckIcon /> : index + 1}</div><div className="trace-card"><span className="step-label">Step {index + 1}</span><strong>{metadata.title}</strong><p>{traceEntry?.public_detail ?? metadata.idle}</p><span className={traceEntry ? "confirmed-text" : "pending-text"}>{traceEntry ? "Confirmed" : "Pending"}</span></div></li>;
        })}</ol>
        <div className={`trace-note ${receipt ? "receipt" : ""}`}>{receipt ? <><CheckIcon />Reader verified action <strong>{receipt.action_id.slice(0, 8)}</strong><br />{receipt.readiness_from} → {receipt.readiness_to}</> : revision ? revision.packet.summary : "The command desk exposes only trustworthy workflow state—never raw SQL, endpoints, or credentials."}</div>
        {error && <p className="error" role="alert">{error}</p>}
        <button className="primary-action" onClick={receipt ? undefined : revision ? createFollowup : applyRevision} disabled={!actionReady || busy || Boolean(receipt)}>{receipt ? "Follow-up created" : busy ? "Working…" : revision ? "Create follow-up" : actionReady ? "Apply revision" : "Runtime unavailable"}</button>
      </aside>
    </section>
  </main>;
}
