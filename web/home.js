/* home.js — shared wiring for index.html (hero only) and personas.html.
   Each page carries only a subset of these elements, so every hook is
   guarded. Nav and CTA links are plain <a href> now and need no JS. */

// personas.html — a card click routes to results (results.js reads the param).
document.querySelectorAll(".p-card").forEach((card) => {
  card.addEventListener("click", () => {
    location.href = `results.html?persona=${card.dataset.persona}`;
  });
});

// personas.html — free-text search.
const input = document.getElementById("describe-input");
if (input) {
  const button = document.getElementById("describe-go");
  const feedback = document.getElementById("describe-feedback");
  const go = async () => {
    if (!input.value.trim()) { input.focus(); return; }
    const query = input.value.trim();
    button.disabled = true;
    button.textContent = "Finding...";
    let profile = null;
    try {
      const response = await fetch("/api/parse", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      if (data && data.blocked) {
        if (feedback) {
          feedback.textContent = data.message || "I can help you choose a Galaxy phone. Tell me your budget and priorities.";
          feedback.hidden = false;
        }
        button.disabled = false;
        button.textContent = "Find my Galaxy";
        return;
      }
      profile = data && data.profile;
    } catch (_) {
      // Local extraction on results.html remains the offline fallback.
    }
    const params = new URLSearchParams({ q: query });
    if (profile) params.set("profile", JSON.stringify(profile));
    location.href = `results.html?${params.toString()}`;
  };
  button.addEventListener("click", go);
  input.addEventListener("keydown", (e) => { if (e.key === "Enter") go(); });
}
