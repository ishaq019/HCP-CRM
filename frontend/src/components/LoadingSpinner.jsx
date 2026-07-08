import React from "react";
export default function LoadingSpinner({ label = "Loading" }) {
  return (
    <span className="spinnerWrap" aria-live="polite">
      <span className="spinner" aria-hidden="true" />
      {label}
    </span>
  );
}
