// api.jsx
import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({ baseURL: BASE_URL });

export default api;

export async function searchInternships({ query, location, page = 1 }) {
  const params = new URLSearchParams({ query, page });
  if (location) params.append("location", location);
  const res = await fetch(`${BASE_URL}/internships/search?${params}`);
  if (!res.ok) throw new Error("Failed to fetch internships");
  return res.json();
}

export async function matchInternships({ field, skills, location, page = 1 }) {
  const params = new URLSearchParams({ field, page });
  if (skills) params.append("skills", skills);
  if (location) params.append("location", location);
  const token = localStorage.getItem("token");
  const res = await fetch(`${BASE_URL}/internships/match?${params}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  });
  if (!res.ok) throw new Error("Failed to fetch matched internships");
  return res.json();
}