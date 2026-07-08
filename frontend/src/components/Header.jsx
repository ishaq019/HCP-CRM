import React from "react";
import { Activity, ShieldCheck } from "lucide-react";

export default function Header() {
  return (
    <header className="topbar topbarHero">
      <div className="topbarCopy">
        <p className="eyebrow">AI-first CRM module</p>
        <h1>Capture HCP visits and turn them into action-ready records</h1>
        <p className="headerCopy">A focused workspace for structured logging, AI-assisted drafting, and fast follow-up tracking.</p>
      </div>
      <div className="topbarPills statusStack">
        <span><Activity size={16} /> LangGraph workflow</span>
        <span><ShieldCheck size={16} /> Groq ready</span>
      </div>
    </header>
  );
}
