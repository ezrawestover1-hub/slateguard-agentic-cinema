import { useMemo, useState } from "react";
import type { ImpactPulse, ReceiptResponse, RevisionResponse } from "./api";

type ReviewWorkspaceProps = {
  actionReady: boolean;
  busy: boolean;
  busyLabel: string | null;
  error: string | null;
  pulse: ImpactPulse | null;
  revision: RevisionResponse | null;
  receipt: ReceiptResponse | null;
  onReview: () => void;
  onFollowUp: () => void;
  onReset: () => void;
};

const baselineEvidence = [
  { id: "ev-dailies-11-blue", title: "Scene 11 dailies", detail: "Captured continuity reference", note: "Footage already establishes the blue jacket before this scene.", kind: "Continuity" },
  { id: "ev-call-sheet-13", title: "Scene 13 call sheet", detail: "Next scheduled dependency", note: "Wardrobe is required before the next scheduled exterior unit.", kind: "Schedule" },
  { id: "ev-call-sheet-14", title: "Scene 14 call sheet", detail: "Next scheduled dependency", note: "Wardrobe is required before the next scheduled exterior unit.", kind: "Schedule" },
];

const stageCopy = ["Scope", "Evidence", "Decision", "Follow-up"];

function Icon({ name, size = 18 }: { name: "check" | "chevron" | "film" | "calendar" | "shield" | "bookmark" | "plus" | "arrow" | "clock" | "users"; size?: number }) {
  const common = { width: size, height: size, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: 1.8, strokeLinecap: "round" as const, strokeLinejoin: "round" as const, "aria-hidden": true };
  if (name === "check") return <svg {...common}><path d="m5 12 4.2 4L19 6.8" /></svg>;
  if (name === "chevron") return <svg {...common}><path d="m9 18 6-6-6-6" /></svg>;
  if (name === "film") return <svg {...common}><rect x="3" y="5" width="14" height="14" rx="2" /><path d="m17 10 4-2v8l-4-2" /><path d="M7 5v14" /></svg>;
  if (name === "calendar") return <svg {...common}><rect x="3" y="5" width="18" height="16" rx="2" /><path d="M7 3v4M17 3v4M3 10h18" /></svg>;
  if (name === "shield") return <svg {...common}><path d="M12 3 20 6v5c0 5.1-3.4 8.7-8 10-4.6-1.3-8-4.9-8-10V6l8-3Z" /><path d="m8.5 12 2.2 2.2 4.8-5" /></svg>;
  if (name === "bookmark") return <svg {...common}><path d="M6 4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18l-6-3-6 3V4Z" /></svg>;
  if (name === "plus") return <svg {...common}><path d="M12 5v14M5 12h14" /></svg>;
  if (name === "arrow") return <svg {...common}><path d="M5 12h14M13 6l6 6-6 6" /></svg>;
  if (name === "clock") return <svg {...common}><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3.5 2" /></svg>;
  return <svg {...common}><path d="M16 20v-1.5a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4V20" /><circle cx="9.5" cy="7" r="3.5" /><path d="M17 11a3 3 0 0 0 0-6M21 20v-1.5a4 4 0 0 0-2.7-3.8" /></svg>;
}

function StageRail({ stage }: { stage: number }) {
  return <ol className="stage-rail" aria-label="Review progress">
    {stageCopy.map((label, index) => {
      const number = index + 1;
      const completed = number < stage;
      const current = number === stage;
      return <li className={`${completed ? "complete" : ""} ${current ? "current" : ""}`} key={label}>
        <span className="stage-dot">{completed ? <Icon name="check" size={15} /> : number}</span>
        <span>{label}</span>
      </li>;
    })}
  </ol>;
}

function Queue({ saved, onSaved }: { saved: boolean; onSaved: () => void }) {
  return <aside className="review-queue" aria-label="Change queue">
    <div className="queue-heading"><div><span className="eyebrow">Production changes</span><h2>Change queue</h2></div><span className="queue-count">1</span></div>
    <button className="queue-item selected" type="button" aria-current="page">
      <span className="queue-status">Review now</span>
      <strong>Scene 12 · Wardrobe continuity</strong>
      <span className="queue-change">Blue jacket <span>→</span> Black jacket</span>
      <span className="queue-meta"><Icon name="clock" size={15} />Current production window</span>
      <Icon name="chevron" size={18} />
    </button>
    <div className="queue-note"><Icon name="shield" size={17} /><p>This public proof is deliberately scoped to one supported production change.</p></div>
    <button className={`save-link ${saved ? "saved" : ""}`} type="button" onClick={onSaved}><Icon name="bookmark" size={17} />{saved ? "Saved for this session" : "Save review for later"}</button>
  </aside>;
}

function EvidenceList({ citedIds }: { citedIds: string[] }) {
  const [openId, setOpenId] = useState<string | null>(null);
  const evidence = useMemo(() => baselineEvidence.filter((item) => citedIds.includes(item.id)), [citedIds]);
  return <section className="evidence-section" aria-labelledby="evidence-heading">
    <div className="section-heading"><div><span className="eyebrow">Curated ClickHouse evidence</span><h2 id="evidence-heading">Why this needs a decision</h2><p>Only relevant, current production records are included in the review.</p></div><span className="evidence-count">{evidence.length} cited</span></div>
    <div className="evidence-list">
      {evidence.map((item, index) => {
        const expanded = openId === item.id;
        return <article className={`evidence-item ${expanded ? "expanded" : ""}`} key={item.id}>
          <span className="evidence-order">{index + 1}</span>
          <span className="evidence-type">{item.kind === "Schedule" ? <Icon name="calendar" size={19} /> : <Icon name="film" size={19} />}</span>
          <div><strong>{item.title}</strong><span>{item.detail}</span>{expanded && <p>{item.note}</p>}</div>
          <span className="evidence-state"><Icon name="check" size={15} />Cited</span>
          <button className="disclosure" type="button" aria-label={`Show ${item.title} detail`} aria-expanded={expanded} onClick={() => setOpenId(expanded ? null : item.id)}><Icon name="chevron" size={18} /></button>
        </article>;
      })}
    </div>
  </section>;
}

function ContextRail({ pulse, owners }: { pulse: ImpactPulse | null; owners: string[] }) {
  const [noteOpen, setNoteOpen] = useState(false);
  return <aside className="context-rail" aria-label="Decision context">
    <div className="context-heading"><span className="eyebrow">Live decision context</span><h2>What changes next</h2></div>
    <section className="context-card"><div className="card-title"><strong>Affected scenes</strong><span>{pulse?.affected_scenes ?? "…"}</span></div><div className="scene-context"><b>11</b><p><strong>Prior footage</strong><span>Captured · continuity reference</span></p></div><div className="scene-context"><b>13–14</b><p><strong>Scheduled next</strong><span>Wardrobe-dependent call sheets</span></p></div></section>
    <section className="context-card risk-card"><div className="card-title"><strong>Schedule risk</strong><span className="risk-badge">At risk</span></div><p>Unresolved continuity may affect the next wardrobe-dependent block.</p><div className="context-stat"><span>Relevant records</span><strong>{pulse?.relevant_evidence_records ?? "…"}</strong></div></section>
    <section className="context-card owner-card"><div className="card-title"><strong>Human owners</strong><Icon name="users" size={18} /></div><p>Recommended owners can make or reject the follow-up.</p>{owners.map((owner, index) => <div className="owner-line" key={owner}><span>{owner.split(" ").map((part) => part[0]).join("")}</span><p><strong>{owner}</strong><small>{index === 0 ? "Decision owner" : "Consulted"}</small></p><Icon name="check" size={17} /></div>)}</section>
    <button className="add-note" type="button" onClick={() => setNoteOpen(!noteOpen)}><Icon name="plus" size={17} />{noteOpen ? "Hide review note" : "Add review note"}</button>
    {noteOpen && <textarea className="review-note" aria-label="Review note" placeholder="Record context for this review session…" />}
  </aside>;
}

function DecisionDock({ actionReady, busy, busyLabel, revision, receipt, onReview, onFollowUp, onReset }: Pick<ReviewWorkspaceProps, "actionReady" | "busy" | "busyLabel" | "revision" | "receipt" | "onReview" | "onFollowUp" | "onReset">) {
  const verified = Boolean(receipt);
  const reviewed = Boolean(revision);
  const title = verified ? "Follow-up verified" : reviewed ? "Ready for human decision" : "Start a controlled review";
  const detail = verified ? `${receipt?.readiness_from} → ${receipt?.readiness_to}. The reader path verified the recorded action.` : reviewed ? "Evidence is grounded. Confirm the recommended human follow-up when you are ready." : "Run the protected revision workflow to produce a grounded change packet.";
  const label = verified ? "Start another review" : reviewed ? "Create recommended follow-up" : "Review this change";
  const action = verified ? onReset : reviewed ? onFollowUp : onReview;
  const activeTitle = busy ? busyLabel ?? "Running a controlled review" : title;
  const activeDetail = busy ? "This is a live, bounded evidence workflow. Keep this page open while SlateGuard returns a decision packet." : detail;
  return <footer className="decision-dock" aria-live="polite"><div className={`dock-icon ${verified ? "verified" : ""} ${busy ? "working" : ""}`}>{verified ? <Icon name="check" size={21} /> : busy ? <Icon name="clock" size={21} /> : <Icon name="users" size={22} />}</div><div className="dock-copy"><strong>{activeTitle}</strong><p>{activeDetail}</p></div><button className="dock-action" type="button" onClick={action} disabled={!actionReady || busy}><span>{busy ? "Review in progress" : label}</span><Icon name={verified ? "arrow" : "chevron"} size={19} /></button></footer>;
}

export function ReviewWorkspace({ actionReady, busy, busyLabel, error, pulse, revision, receipt, onReview, onFollowUp, onReset }: ReviewWorkspaceProps) {
  const [saved, setSaved] = useState(false);
  const citedIds = revision?.packet.cited_evidence_ids ?? baselineEvidence.map((item) => item.id);
  const owners = receipt?.owners ?? revision?.packet.recommended_owners ?? ["Wardrobe", "Assistant Director"];
  const stage = receipt ? 4 : revision ? 3 : 2;
  const readiness = receipt?.readiness_to ?? revision?.evaluation.readiness ?? "Evidence review";
  return <main className="review-app">
    <header className="app-header"><a className="wordmark" href="#review" aria-label="SlateGuard review workspace"><span className="mark">S</span>SLATE<span>GUARD</span></a><div className="project-switcher"><span>Project</span><strong>Northern Lights</strong></div><div className="runtime-status"><Icon name="check" size={17} />{actionReady ? "Verified runtime" : "Checking runtime"}</div></header>
    <div className="review-layout" id="review"><Queue saved={saved} onSaved={() => setSaved(!saved)} /><section className="decision-workspace" aria-live="polite"><StageRail stage={stage} /><div className="brief-heading"><span className="eyebrow">Active review · SG-12</span><h1>Decision brief</h1><p>A wardrobe change is proposed for Scene 12. Review the current production evidence before creating a human-owned follow-up.</p></div><div className="change-summary"><div><span>Proposed change</span><strong>Blue jacket <b>→</b> Black jacket</strong></div><div><span>Current readiness</span><strong className={receipt ? "positive" : "caution"}>{readiness}</strong></div><div><span>Evidence scope</span><strong>{pulse ? `${pulse.relevant_evidence_records} relevant records` : "Loading current records"}</strong></div></div><EvidenceList citedIds={citedIds} />{revision && <section className="recommendation"><span className="eyebrow">Grounded recommendation</span><strong>{revision.packet.summary}</strong><p>The packet cites only the evidence shown above and keeps final action with the production team.</p></section>}{error && <p className="review-error" role="alert">{error}</p>}</section><ContextRail pulse={pulse} owners={owners} /></div><DecisionDock actionReady={actionReady} busy={busy} busyLabel={busyLabel} revision={revision} receipt={receipt} onReview={onReview} onFollowUp={onFollowUp} onReset={onReset} /></main>;
}
