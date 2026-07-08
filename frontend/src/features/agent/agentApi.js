const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

async function request(path, payload) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      detail = body.detail || detail;
      if (Array.isArray(detail)) detail = detail.map((item) => item.msg).join(", ");
    } catch {
      detail = response.statusText || detail;
    }
    throw new Error(detail);
  }
  return response.json();
}

export const agentApi = {
  chat: (payload) => request("/agent/chat", payload),
  logInteraction: (payload) => request("/agent/log-interaction", payload),
  editInteraction: (payload) => request("/agent/edit-interaction", payload),
  summarize: (payload) => request("/agent/summarize", payload),
  suggestFollowup: (payload) => request("/agent/suggest-followup", payload),
  extractInsights: (payload) => request("/agent/extract-insights", payload),
};
