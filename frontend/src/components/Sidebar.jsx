import React from "react";
import { Bot, ClipboardList, LayoutDashboard } from "lucide-react";
import { NavLink } from "react-router-dom";

const links = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard },
  { to: "/log", label: "Log Interaction", icon: Bot },
  { to: "/interactions", label: "Interactions", icon: ClipboardList },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <span className="brandMark">AI</span>
        <div>
          <strong>HCP CRM</strong>
          <small>Field intelligence</small>
        </div>
      </div>
      <div className="sidebarCard">
        <p className="eyebrow sidebarEyebrow">Workflow</p>
        <strong>Log, review, and act</strong>
        <p>Keep every conversation searchable, editable, and ready for follow-up in one place.</p>
      </div>
      <nav className="navRail">
        {links.map(({ to, label, icon: Icon }) => (
          <NavLink key={to} to={to} className={({ isActive }) => `navLink ${isActive ? "active" : ""}`}>
            <Icon size={18} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>
      <div className="sidebarCard sidebarCardAccent">
        <p className="eyebrow sidebarEyebrow">Live assistant</p>
        <strong>Groq + LangGraph</strong>
        <p>Structured form entry, natural-language extraction, summaries, follow-up suggestions, and insights.</p>
      </div>
    </aside>
  );
}
