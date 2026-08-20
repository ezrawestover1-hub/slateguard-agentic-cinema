export type RuntimeStatus = "ready" | "configuration_pending";
export type ChangeInput = { scene_id: string; fact_type: "wardrobe" | "prop" | "set dressing" | "blocking" | "schedule"; old_value: string; new_value: string };
export type TraceEntry = { step: string; status: string; public_detail: string };
export type ImpactPulse = { scope: string; relevant_evidence_records: number; active_scene_records: number; affected_scenes: number; scheduled_dependencies: number };
export type RevisionResponse = { revision_id: string; change: ChangeInput; packet: { status: "ready" | "review_required"; summary: string; cited_evidence_ids: string[]; recommended_owners: string[]; distinguishes_unknowns: boolean }; evaluation: { readiness: string; can_create_followup: boolean; reason: string }; trace: TraceEntry[] };
export type ReceiptResponse = { action_id: string; readiness_from: string; readiness_to: string; owners: string[]; trace: TraceEntry[] };
async function request<T>(path: string, init?: RequestInit): Promise<T> { const response = await fetch(path, init); if (!response.ok) throw new Error(`Request failed (${response.status}).`); return response.json() as Promise<T>; }
export const api = {
  runtime: () => request<{ state: RuntimeStatus }>("/api/runtime-status"),
  impactPulse: () => request<ImpactPulse>("/api/impact-pulse"),
  reset: () => request<{ state: string }>("/api/demo/reset", { method: "POST" }),
  revise: (change: ChangeInput, idempotencyKey: string) => request<RevisionResponse>("/api/revisions", { method: "POST", headers: { "Content-Type": "application/json", "Idempotency-Key": idempotencyKey }, body: JSON.stringify(change) }),
  followup: (revisionId: string, idempotencyKey: string) => request<ReceiptResponse>(`/api/revisions/${revisionId}/follow-up`, { method: "POST", headers: { "Content-Type": "application/json", "Idempotency-Key": idempotencyKey }, body: JSON.stringify({ reviewed_evidence: true }) }),
};
