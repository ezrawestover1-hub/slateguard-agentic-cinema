import { useEffect, useState } from "react";
import { api, ImpactPulse, ReceiptResponse, RevisionResponse, RuntimeStatus } from "./api";
import { ReviewWorkspace } from "./review-workspace";

type RuntimeState = "loading" | RuntimeStatus | "unavailable";

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

  async function applyRevision() {
    setBusy(true); setError(null); setReceipt(null);
    try {
      await api.reset();
      setRevision(await api.revise(crypto.randomUUID()));
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to analyze this revision.");
    } finally {
      setBusy(false);
    }
  }

  async function createFollowup() {
    if (!revision) return;
    setBusy(true); setError(null);
    try {
      setReceipt(await api.followup(revision.revision_id, crypto.randomUUID()));
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to create the follow-up.");
    } finally {
      setBusy(false);
    }
  }

  async function resetReview() {
    setBusy(true); setError(null);
    try {
      await api.reset();
      setRevision(null);
      setReceipt(null);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Unable to reset this review.");
    } finally {
      setBusy(false);
    }
  }

  return <ReviewWorkspace
    actionReady={runtime === "ready"}
    busy={busy}
    error={error}
    pulse={pulse}
    revision={revision}
    receipt={receipt}
    onReview={applyRevision}
    onFollowUp={createFollowup}
    onReset={resetReview}
  />;
}
