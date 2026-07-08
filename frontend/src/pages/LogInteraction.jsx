import React from "react";
import { Bot, ClipboardPenLine } from "lucide-react";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import ChatLogger from "../components/ChatLogger";
import InteractionForm, { emptyInteraction } from "../components/InteractionForm";
import { createInteraction } from "../features/interactions/interactionSlice";

export default function LogInteraction() {
  const dispatch = useDispatch();
  const [mode, setMode] = useState("form");
  const [form, setForm] = useState(emptyInteraction);
  const { status, error, success } = useSelector((state) => state.interactions);

  const save = async (payload) => {
    await dispatch(createInteraction(payload)).unwrap();
    setForm(emptyInteraction);
  };

  return (
    <div className="pageStack">
      <section className="heroCard compactHero">
        <div className="heroCopy">
          <p className="eyebrow heroEyebrow">Interaction capture</p>
          <h1>Structured form for precision, AI chat for speed.</h1>
          <p className="heroText">Use the clean form when details are known, or paste conversational notes and review the generated draft before saving.</p>
        </div>
        <div className="heroDeck compactDeck">
          <div className="heroMetric">
            <span>Capture mode</span>
            <strong>{mode === "form" ? "Form" : "AI chat"}</strong>
          </div>
          <div className="heroMetric">
            <span>Save status</span>
            <strong>{status === "loading" ? "Saving" : "Ready"}</strong>
          </div>
        </div>
      </section>
      <section className="modeHeader">
        <div>
          <p className="eyebrow">Interaction capture</p>
          <h2>Choose structured entry or AI chat extraction</h2>
        </div>
        <div className="segmented">
          <button className={mode === "form" ? "active" : ""} onClick={() => setMode("form")}><ClipboardPenLine size={16} /> Form</button>
          <button className={mode === "chat" ? "active" : ""} onClick={() => setMode("chat")}><Bot size={16} /> AI chat</button>
        </div>
      </section>
      {success && <div className="alert success">{success}</div>}
      {error && <div className="alert error">{error}</div>}
      {mode === "form" ? (
        <section className="panel">
          <h2>Structured form</h2>
          <InteractionForm value={form} onChange={setForm} onSubmit={save} loading={status === "loading"} />
        </section>
      ) : (
        <ChatLogger />
      )}
    </div>
  );
}
