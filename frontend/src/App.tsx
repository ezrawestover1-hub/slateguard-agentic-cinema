import { useEffect, useState } from "react";
import { api, ChangeInput, ImpactPulse, ReceiptResponse, RevisionResponse, RuntimeStatus } from "./api";
import { ReviewWorkspace } from "./review-workspace";

type RuntimeState = "loading" | RuntimeStatus | "unavailable";
const initialChange: ChangeInput = { scene_id: "scene-12", fact_type: "wardrobe", old_value: "blue jacket", new_value: "black jacket" };

export function App() {
  const [runtime, setRuntime] = useState<RuntimeState>("loading");
  const [pulse, setPulse] = useState<ImpactPulse | null>(null);
  const [revision, setRevision] = useState<RevisionResponse | null>(null);
  const [change, setChange] = useState<ChangeInput>(initialChange);
  const [receipt, setReceipt] = useState<ReceiptResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const [busyLabel, setBusyLabel] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.runtime().then((body) => setRuntime(body.state)).catch(() => setRuntime("unavailable"));
    api.impactPulse().then(setPulse).catch(() => setPulse(null));
  }, []);

  async function applyRevision(nextChange: ChangeInput) {
    setBusy(true); setBusyLabel("Checking the current production memory"); setError(null); setReceipt(null);
    try {
      await api.reset();
      setBusyLabel("Gathering curated ClickHouse evidence");
      const result = await api.revise(nextChange, crypto.randomUUID());
      setChange(result.change);
      setRevision(result);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to analyze this revision.");
    } finally {
      setBusy(false); setBusyLabel(null);
    }
  }

  async function createFollowup() {
    if (!revision) return;
    setBusy(true); setBusyLabel("Recording the human-owned follow-up"); setError(null);
    try {
      setReceipt(await api.followup(revision.revision_id, crypto.randomUUID()));
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to create the follow-up.");
    } finally {
      setBusy(false); setBusyLabel(null);
    }
  }

  async function resetReview() {
    setBusy(true); setBusyLabel("Preparing a fresh controlled review"); setError(null);
    try {
      await api.reset();
      setRevision(null);
      setReceipt(null);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to reset this review.");
    } finally {
      setBusy(false); setBusyLabel(null);
    }
  }

  return <ReviewWorkspace
    actionReady={runtime === "ready"}
    busy={busy}
    busyLabel={busyLabel}
    error={error}
    change={change}
    pulse={pulse}
    revision={revision}
    receipt={receipt}
    onReview={applyRevision}
    onFollowUp={createFollowup}
    onReset={resetReview}
  />;
}
