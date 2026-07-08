import React from "react";
import { SendHorizontal, Sparkles } from "lucide-react";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { clearDraft, sendChatMessage } from "../features/agent/agentSlice";
import { createInteraction } from "../features/interactions/interactionSlice";
import InteractionForm, { emptyInteraction, normalizePayload } from "./InteractionForm";
import LoadingSpinner from "./LoadingSpinner";

const quickPrompts = [
  {
    label: "Apollo Hospital visit",
    text: "Met Dr. Sharma today at Apollo Hospital. Discussed CardioPlus. He seemed positive and asked for samples. Follow up next Monday.",
  },
  {
    label: "Positive product interest",
    text: "Dr. Rao reviewed the latest data, was positive about the efficacy signal, and requested starter samples for next week.",
  },
  {
    label: "Conference follow-up",
    text: "Spoke with Dr. Meera after the cardiology conference. She wants a recap, product details, and a follow-up call in two days.",
  },
];

export default function ChatLogger() {
  const dispatch = useDispatch();
  const { chatMessages, draft, status, error } = useSelector((state) => state.agent);
  const [message, setMessage] = useState("Met Dr. Sharma today at Apollo Hospital. Discussed CardioPlus. He seemed positive and asked for samples. Follow up next Monday.");
  const [editableDraft, setEditableDraft] = useState(null);
  const loading = status === "loading";

  const submitMessage = async (event) => {
    event.preventDefault();
    if (!message.trim()) return;
    const result = await dispatch(sendChatMessage({ message, conversation: chatMessages }));
    if (result.payload?.data?.draft) setEditableDraft({ ...emptyInteraction, ...result.payload.data.draft });
    setMessage("");
  };

  const saveDraft = async (payload) => {
    await dispatch(createInteraction(normalizePayload(payload))).unwrap();
    dispatch(clearDraft());
    setEditableDraft(null);
  };

  return (
    <div className="splitPanel">
      <section className="panel">
        <div className="sectionTitle">
          <Sparkles size={18} />
          <h2>AI chat logger</h2>
        </div>
        <p className="formHint">Paste natural notes and let the agent prepare a structured draft you can edit before saving.</p>
        <div className="promptRow">
          {quickPrompts.map((prompt) => (
            <button key={prompt.label} type="button" className="promptChip" onClick={() => setMessage(prompt.text)}>
              {prompt.label}
            </button>
          ))}
        </div>
        <div className="chatWindow">
          {chatMessages.length === 0 && <p className="emptyState">Describe the interaction naturally and the LangGraph agent will prepare a structured draft.</p>}
          {chatMessages.map((item, index) => (
            <div key={`${item.role}-${index}`} className={`message ${item.role}`}>
              {item.content}
            </div>
          ))}
        </div>
        {error && <div className="alert error">{error}</div>}
        <form className="chatComposer" onSubmit={submitMessage}>
          <textarea value={message} onChange={(event) => setMessage(event.target.value)} rows={3} />
          <button className="primaryButton" type="submit" disabled={loading}>
            <SendHorizontal size={17} />
            {loading ? <LoadingSpinner label="Extracting" /> : "Extract draft"}
          </button>
        </form>
      </section>
      <section className="panel">
        <h2>Review extracted draft</h2>
        {!draft && !editableDraft && <p className="emptyState">The editable AI draft will appear here before anything is saved.</p>}
        {(draft || editableDraft) && (
          <InteractionForm
            value={editableDraft || draft}
            onChange={setEditableDraft}
            onSubmit={saveDraft}
            submitLabel="Save reviewed draft"
            loading={loading}
          />
        )}
      </section>
    </div>
  );
}
