import React from "react";
import { useEffect } from "react";
import { useMemo, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Search } from "lucide-react";
import InteractionDetails from "../components/InteractionDetails";
import InteractionList from "../components/InteractionList";
import LoadingSpinner from "../components/LoadingSpinner";
import { fetchInteractions } from "../features/interactions/interactionSlice";

export default function Interactions() {
  const dispatch = useDispatch();
  const { items, status, error, success } = useSelector((state) => state.interactions);
  const [search, setSearch] = useState("");

  useEffect(() => {
    dispatch(fetchInteractions());
  }, [dispatch]);

  const filteredItems = useMemo(() => {
    const query = search.trim().toLowerCase();
    if (!query) return items;
    return items.filter((item) => (
      [item.hcp_name, item.organization, item.hcp_specialty, item.discussion_summary, item.next_best_action]
        .filter(Boolean)
        .join(" ")
        .toLowerCase()
        .includes(query)
    ));
  }, [items, search]);

  return (
    <div className="pageStack">
      {status === "loading" && <LoadingSpinner />}
      {success && <div className="alert success">{success}</div>}
      {error && <div className="alert error">{error}</div>}
      <section className="panel workspaceHeader">
        <div>
          <p className="eyebrow">Saved interactions</p>
          <h2>Search, edit, and manage every visit from one screen</h2>
          <p className="formHint">Filter by HCP, organization, specialty, or notes to find the right record quickly.</p>
        </div>
        <label className="searchField">
          <Search size={16} />
          <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search interactions" />
        </label>
      </section>
      <div className="interactionsLayout">
        <section className="panel">
          <div className="sectionTitle sectionTitleCompact">
            <h2>Saved interactions</h2>
            <span className="metaChip">Showing {filteredItems.length} of {items.length}</span>
          </div>
          <InteractionList items={filteredItems} />
        </section>
        <InteractionDetails />
      </div>
    </div>
  );
}
