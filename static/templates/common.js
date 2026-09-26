// Shared helpers for every template: data loading, formatting, escaping.
window.AIW = (() => {
  const ORG_COLORS = {
    "Anthropic": "#d97757", "OpenAI": "#10a37f", "Google": "#4285f4", "Meta": "#0866ff",
    "Mistral": "#fa520f", "Hugging Face": "#e6a100", "NVIDIA": "#76b900", "Microsoft": "#7f5af0",
    "Berkeley": "#3b6fb6", "Hacker News": "#ff6600",
  };
  const store = {
    get(k, d) { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
  };
  const lastVisit = store.get("ainews.lastVisit", null);
  // Gallery previews run in iframes: don't let them count as a visit.
  if (window.self === window.top) store.set("ainews.lastVisit", new Date().toISOString());

  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const safeUrl = (u) => (/^https?:\/\//i.test(u || "") ? u : "#");
  const when = (p) => new Date(p.date || p.first_seen);
  const isNew = (p) => !!lastVisit && new Date(p.first_seen) > new Date(lastVisit);
  const color = (org) => ORG_COLORS[org] || "#888";
  const host = (u) => { try { return new URL(u).hostname.replace(/^www\./, ""); } catch { return ""; } };

  function ago(d) {
    const s = (Date.now() - d) / 1000;
    if (s < 3600) return `${Math.max(1, Math.round(s / 60))}m`;
    if (s < 86400) return `${Math.round(s / 3600)}h`;
    if (s < 86400 * 7) return `${Math.round(s / 86400)}d`;
    return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
  }

  function dayLabel(d) {
    const start = (x) => new Date(x.getFullYear(), x.getMonth(), x.getDate());
    const diff = Math.round((start(new Date()) - start(d)) / 86400000);
    if (diff <= 0) return "Today";
    if (diff === 1) return "Yesterday";
    if (diff < 7) return d.toLocaleDateString(undefined, { weekday: "long" });
    return d.toLocaleDateString(undefined, { month: "long", day: "numeric" });
  }

  async function load(refresh = false) {
    const res = await fetch(refresh ? "/api/refresh" : "/api/news", { method: refresh ? "POST" : "GET" });
    const data = await res.json();
    data.labs = data.posts.filter((p) => p.source !== "hn").sort((a, b) => when(b) - when(a));
    data.hn = data.posts.filter((p) => p.source === "hn").sort((a, b) => b.points - a.points);
    data.orgs = [...new Set(data.sources.filter((s) => s.id !== "hn").map((s) => s.org))];
    return data;
  }

  const matches = (p, q) => !q || `${p.title} ${p.summary || ""} ${p.source_name}`.toLowerCase().includes(q.toLowerCase());

  return { ORG_COLORS, store, esc, safeUrl, when, isNew, color, host, ago, dayLabel, load, matches };
})();
