const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      detail = body.detail || detail;
      if (Array.isArray(detail)) {
        detail = detail.map((item) => item.msg).join(", ");
      }
    } catch {
      detail = response.statusText || detail;
    }
    throw new Error(detail);
  }
  if (response.status === 204) return null;
  return response.json();
}

function queryString(params = {}) {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      searchParams.append(key, String(value));
    }
  });
  const serialized = searchParams.toString();
  return serialized ? `?${serialized}` : "";
}

export const interactionApi = {
  list: () => request("/interactions"),
  query: (params) => request(`/interactions/query${queryString(params)}`),
  get: (id) => request(`/interactions/${id}`),
  create: (payload) => request("/interactions", { method: "POST", body: JSON.stringify(payload) }),
  update: (id, payload) => request(`/interactions/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  remove: (id) => request(`/interactions/${id}`, { method: "DELETE" }),
};
