import React from "react";
import { Bot, FilePenLine, Lightbulb, MessageSquarePlus, Sparkles } from "lucide-react";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  runEditTool,
  runFollowupTool,
  runInsightsTool,
  runLogTool,
  runSummaryTool,
} from "../features/agent/agentSlice";

const sampleText = "Met Dr. Meera Rao at City Heart Clinic. Discussed CardioPlus and trial outcomes. She was positive, asked for starter samples, and wants follow-up early next week.";

export default function ToolDemoPanel() {
  const dispatch = useDispatch();
  const { items } = useSelector((state) => state.interactions);
  const { toolResult, status, error } = useSelector((state) => state.agent);
  const [interactionId, setInteractionId] = useState("");
  const [text, setText] = useState(sampleText);
  const loading = status === "loading";

  const idPayload = interactionId ? Number(interactionId) : null;

  const buttons = [
    { label: "Log Interaction", icon: MessageSquarePlus, action: () => dispatch(runLogTool({ message: text })) },
    { label: "Edit Interaction", icon: FilePenLine, action: () => dispatch(runEditTool({ interaction_id: idPayload, message: text })) },
    { label: "Summarize", icon: Sparkles, action: () => dispatch(runSummaryTool({ interaction_id: idPayload, raw_notes: text })) },
    {
      label: "Suggest Follow-up",
      icon: Lightbulb,
      action: () => dispatch(runFollowupTool({
        interaction_id: idPayload,
        interaction_data: idPayload ? null : {
          discussion_summary: text,
          sentiment: "Positive",
          priority: "Medium",
          samples_requested: "starter samples",
        },
      })),
    },
    { label: "Extract Insights", icon: Bot, action: () => dispatch(runInsightsTool({ interaction_id: idPayload, raw_notes: text })) },
  ];

  return (
    <section className="panel toolPanel">
      <div className="sectionTitle">
        <Bot size={18} />
        <h2>LangGraph tool demo</h2>
      </div>
      <p className="formHint">Run the same AI tools the app uses in production. Pick a saved interaction or let the sample text drive the flow.</p>
      <div className="toolInputs">
        <label>
          Saved interaction
          <select value={interactionId} onChange={(event) => setInteractionId(event.target.value)}>
            <option value="">Use text only</option>
            {items.map((item) => <option key={item.id} value={item.id}>#{item.id} - {item.hcp_name}</option>)}
          </select>
        </label>
        <label>
          Tool input text
          <textarea rows={4} value={text} onChange={(event) => setText(event.target.value)} />
        </label>
      </div>
      <div className="toolButtons toolButtonsGrid">
        {buttons.map(({ label, icon: Icon, action }) => (
          <button key={label} type="button" className="secondaryButton toolButton" onClick={action} disabled={loading || (label.includes("Edit") && !idPayload)}>
            <Icon size={16} />
            {label}
          </button>
        ))}
      </div>
      {error && <div className="alert error">{error}</div>}
      {toolResult && <pre className="jsonBlock">{JSON.stringify(toolResult, null, 2)}</pre>}
    </section>
  );
}
