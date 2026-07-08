import React from "react";
import { Pencil, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { deleteInteraction, updateInteraction } from "../features/interactions/interactionSlice";
import InteractionForm, { normalizePayload } from "./InteractionForm";

export default function InteractionDetails() {
  const dispatch = useDispatch();
  const { items, selectedId, status } = useSelector((state) => state.interactions);
  const selected = items.find((item) => item.id === selectedId);
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(null);

  useEffect(() => {
    setDraft(selected || null);
    setEditing(false);
  }, [selected]);

  if (!selected) return <p className="emptyState">Select an interaction to view details.</p>;
  const interactionDate = selected.interaction_datetime
    ? new Date(selected.interaction_datetime).toLocaleString([], { dateStyle: "medium", timeStyle: "short" })
    : "Not captured";

  const save = async (payload) => {
    await dispatch(updateInteraction({ id: selected.id, data: normalizePayload(payload) })).unwrap();
    setEditing(false);
  };

  if (editing) {
    return (
      <div className="panel">
        <h2>Edit interaction</h2>
        <InteractionForm value={draft} onChange={setDraft} onSubmit={save} submitLabel="Update interaction" loading={status === "loading"} />
      </div>
    );
  }

  return (
    <div className="panel detailPanel">
      <div className="detailHeader">
        <div>
          <p className="eyebrow">{selected.interaction_type}</p>
          <h2>{selected.hcp_name}</h2>
          <p>{selected.hcp_specialty || "Specialty not captured"} - {selected.organization || "Organization not captured"}</p>
          <div className="detailMeta">
            <span className="metaChip">{interactionDate}</span>
            <span className="metaChip">Sentiment: {selected.sentiment}</span>
            <span className="metaChip">Priority: {selected.priority}</span>
          </div>
        </div>
        <div className="buttonRow">
          <button className="secondaryButton" onClick={() => { setDraft(selected); setEditing(true); }}><Pencil size={16} /> Edit</button>
          <button className="dangerButton" onClick={() => dispatch(deleteInteraction(selected.id))}><Trash2 size={16} /> Delete</button>
        </div>
      </div>
      <div className="metricsGrid detailMetrics">
        <span><strong>Sentiment</strong>{selected.sentiment}</span>
        <span><strong>Priority</strong>{selected.priority}</span>
        <span><strong>Follow-up</strong>{selected.follow_up_required ? "Required" : "Not required"}</span>
      </div>
      <h3>Discussion</h3>
      <p>{selected.discussion_summary}</p>
      <h3>Products and samples</h3>
      <p>{selected.products_discussed || "No product captured"} - {selected.samples_requested || "No samples requested"}</p>
      {selected.ai_summary && (
        <>
          <h3>AI summary</h3>
          <p>{selected.ai_summary}</p>
        </>
      )}
      {selected.next_best_action && (
        <>
          <h3>Next best action</h3>
          <p>{selected.next_best_action}</p>
        </>
      )}
      {selected.ai_insights && (
        <>
          <h3>AI insights</h3>
          <pre className="jsonBlock">{JSON.stringify(selected.ai_insights, null, 2)}</pre>
        </>
      )}
    </div>
  );
}
