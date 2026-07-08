import React from "react";
import { CalendarClock } from "lucide-react";
import { useDispatch, useSelector } from "react-redux";
import { selectInteraction } from "../features/interactions/interactionSlice";

export default function InteractionList({ items: itemsOverride = null, selectedId: selectedIdOverride = null, onSelect = null }) {
  const dispatch = useDispatch();
  const { items, selectedId } = useSelector((state) => state.interactions);
  const listItems = itemsOverride || items;
  const activeId = selectedIdOverride ?? selectedId;

  const handleSelect = onSelect || ((id) => dispatch(selectInteraction(id)));

  if (!listItems.length) return <p className="emptyState">No interactions found for the current search.</p>;

  return (
    <div className="listStack">
      {listItems.map((item) => (
        <button
          key={item.id}
          className={`listItem ${activeId === item.id ? "selected" : ""}`}
          onClick={() => handleSelect(item.id)}
        >
          <div className="listItemTop">
            <strong>{item.hcp_name}</strong>
            <span className={`statusPill statusPill${item.priority}`}>{item.priority}</span>
          </div>
          <span>{item.organization || item.hcp_specialty || "HCP interaction"}</span>
          <div className="listItemMeta">
            <small><CalendarClock size={13} /> {new Date(item.interaction_datetime).toLocaleString()}</small>
            <small>{item.sentiment}</small>
          </div>
        </button>
      ))}
    </div>
  );
}
