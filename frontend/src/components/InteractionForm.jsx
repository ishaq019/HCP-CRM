import React from "react";
import { Save } from "lucide-react";
import LoadingSpinner from "./LoadingSpinner";

export const emptyInteraction = {
  hcp_name: "",
  hcp_specialty: "",
  organization: "",
  interaction_type: "Meeting",
  interaction_datetime: new Date().toISOString().slice(0, 16),
  discussion_summary: "",
  products_discussed: "",
  samples_requested: "",
  follow_up_required: false,
  follow_up_date: "",
  representative_notes: "",
  sentiment: "Neutral",
  priority: "Medium",
};

const interactionTypes = ["Meeting", "Call", "Email", "Conference", "Follow-up", "Other"];
const sentiments = ["Positive", "Neutral", "Negative"];
const priorities = ["Low", "Medium", "High"];

function normalizeForForm(value) {
  if (!value) return "";
  if (typeof value === "string" && value.includes("T")) return value.slice(0, 16);
  return value;
}

export function normalizePayload(data) {
  return {
    ...data,
    interaction_datetime: data.interaction_datetime || new Date().toISOString(),
    follow_up_date: data.follow_up_required && data.follow_up_date ? data.follow_up_date : null,
  };
}

export default function InteractionForm({ value, onChange, onSubmit, submitLabel = "Save interaction", loading = false }) {
  const form = { ...emptyInteraction, ...value };

  const setField = (name, nextValue) => {
    onChange({ ...form, [name]: nextValue });
  };

  return (
    <form className="formGrid" onSubmit={(event) => { event.preventDefault(); onSubmit(normalizePayload(form)); }}>
      <p className="formHint wide">All fields are editable before save. Use the visit timing and follow-up controls to keep the next action obvious.</p>
      <label>
        HCP name
        <input required value={form.hcp_name || ""} onChange={(event) => setField("hcp_name", event.target.value)} />
      </label>
      <label>
        Specialty
        <input value={form.hcp_specialty || ""} onChange={(event) => setField("hcp_specialty", event.target.value)} />
      </label>
      <label>
        Organization
        <input value={form.organization || ""} onChange={(event) => setField("organization", event.target.value)} />
      </label>
      <label>
        Interaction type
        <select value={form.interaction_type || "Meeting"} onChange={(event) => setField("interaction_type", event.target.value)}>
          {interactionTypes.map((type) => <option key={type}>{type}</option>)}
        </select>
      </label>
      <label>
        Date and time
        <input
          required
          type="datetime-local"
          value={normalizeForForm(form.interaction_datetime)}
          onChange={(event) => setField("interaction_datetime", event.target.value)}
        />
      </label>
      <label>
        Sentiment
        <select value={form.sentiment || "Neutral"} onChange={(event) => setField("sentiment", event.target.value)}>
          {sentiments.map((sentiment) => <option key={sentiment}>{sentiment}</option>)}
        </select>
      </label>
      <label>
        Priority
        <select value={form.priority || "Medium"} onChange={(event) => setField("priority", event.target.value)}>
          {priorities.map((priority) => <option key={priority}>{priority}</option>)}
        </select>
      </label>
      <div className="formDivider wide">
        <div>
          <h3>Visit summary</h3>
          <p>Capture the discussion, products, and samples with enough detail to search later.</p>
        </div>
      </div>
      <label className="wide">
        Discussion summary
        <textarea required rows={4} value={form.discussion_summary || ""} onChange={(event) => setField("discussion_summary", event.target.value)} />
      </label>
      <label>
        Products discussed
        <input value={form.products_discussed || ""} onChange={(event) => setField("products_discussed", event.target.value)} />
      </label>
      <label>
        Samples requested
        <input value={form.samples_requested || ""} onChange={(event) => setField("samples_requested", event.target.value)} />
      </label>
      <label className="checkRow">
        <input
          type="checkbox"
          checked={Boolean(form.follow_up_required)}
          onChange={(event) => setField("follow_up_required", event.target.checked)}
        />
        Follow-up required
      </label>
      <div className="formDivider wide">
        <div>
          <h3>Follow-up and notes</h3>
          <p>Keep future actions and rep observations visible without scrolling through the entire record.</p>
        </div>
      </div>
      <label>
        Follow-up date
        <input
          type="datetime-local"
          disabled={!form.follow_up_required}
          value={normalizeForForm(form.follow_up_date)}
          onChange={(event) => setField("follow_up_date", event.target.value)}
        />
      </label>
      <label className="wide">
        Representative notes
        <textarea rows={3} value={form.representative_notes || ""} onChange={(event) => setField("representative_notes", event.target.value)} />
      </label>
      <div className="formActions wide">
        <button className="primaryButton" type="submit" disabled={loading}>
          <Save size={17} />
          {loading ? <LoadingSpinner label="Saving" /> : submitLabel}
        </button>
      </div>
    </form>
  );
}
