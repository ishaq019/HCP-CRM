import React from "react";
import { AlertTriangle, CalendarClock, ClipboardList, Star } from "lucide-react";
import { useEffect } from "react";
import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import ToolDemoPanel from "../components/ToolDemoPanel";
import { fetchInteractions } from "../features/interactions/interactionSlice";

export default function Dashboard() {
  const dispatch = useDispatch();
  const { items, error } = useSelector((state) => state.interactions);

  useEffect(() => {
    dispatch(fetchInteractions());
  }, [dispatch]);

  const today = new Date();
  const followupsDue = items.filter((item) => item.follow_up_required && item.follow_up_date && new Date(item.follow_up_date) <= today);
  const highPriority = items.filter((item) => item.priority === "High");
  const positiveCount = items.filter((item) => item.sentiment === "Positive").length;

  return (
    <div className="pageStack">
      <section className="heroCard dashboardHero">
        <div className="heroCopy">
          <p className="eyebrow heroEyebrow">Field-ready CRM workspace</p>
          <h1>Capture visits faster, surface follow-ups sooner, and keep the AI draft editable.</h1>
          <p className="heroText">Log structured interactions, review extracted notes, and manage every record from a single polished workspace.</p>
          <div className="heroActions">
            <Link to="/log" className="primaryButton">Log interaction</Link>
            <Link to="/interactions" className="secondaryButton">Review records</Link>
          </div>
        </div>
        <div className="heroDeck">
          <div className="heroMetric">
            <span>Saved interactions</span>
            <strong>{items.length}</strong>
          </div>
          <div className="heroMetric">
            <span>Follow-ups due</span>
            <strong>{followupsDue.length}</strong>
          </div>
          <div className="heroMetric">
            <span>High priority</span>
            <strong>{highPriority.length}</strong>
          </div>
          <div className="heroMetric">
            <span>Positive sentiment</span>
            <strong>{positiveCount}</strong>
          </div>
        </div>
      </section>
      {error && <div className="alert error">{error}</div>}
      <section className="statsGrid">
        <div className="statCard"><ClipboardList /><span>Total interactions</span><strong>{items.length}</strong></div>
        <div className="statCard"><CalendarClock /><span>Follow-ups due</span><strong>{followupsDue.length}</strong></div>
        <div className="statCard"><AlertTriangle /><span>High priority HCPs</span><strong>{highPriority.length}</strong></div>
        <div className="statCard"><Star /><span>Positive sentiment</span><strong>{positiveCount}</strong></div>
      </section>
      <section className="panel">
        <h2>Recent interactions</h2>
        {!items.length && <p className="emptyState">Saved interactions will appear here after the first form or AI-assisted log.</p>}
        <div className="recentGrid">
          {items.slice(0, 4).map((item) => (
            <article key={item.id} className="miniCard">
              <strong>{item.hcp_name}</strong>
              <span>{item.organization || item.hcp_specialty || "No organization captured"}</span>
              <p>{item.discussion_summary}</p>
            </article>
          ))}
        </div>
      </section>
      <ToolDemoPanel />
    </div>
  );
}
