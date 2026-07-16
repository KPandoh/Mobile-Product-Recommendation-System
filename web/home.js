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
  const go = () => {
    if (!input.value.trim()) { input.focus(); return; }
    location.href = `results.html?q=${encodeURIComponent(input.value.trim())}`;
  };
  document.getElementById("describe-go").addEventListener("click", go);
  input.addEventListener("keydown", (e) => { if (e.key === "Enter") go(); });
}
