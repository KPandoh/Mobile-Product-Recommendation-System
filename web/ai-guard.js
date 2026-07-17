/* ai-guard.js — quota guardrails for /api/explain and /api/parse.
   Loaded before home.js and results.js on every page so both share one
   circuit breaker via sessionStorage (same tab, resets on tab close).

   The free tier is 20 requests/day PER MODEL. Two things burn it for no
   reason: re-clicking the same persona during a demo rehearsal re-asks a
   question already answered, and once the day's quota is dead the site
   still tries on every render, paying a network round-trip for a call that
   cannot succeed. This file fixes both, client-side, with no backend state. */

const AIGuard = (() => {
  const DOWN_KEY = "gm_ai_down_until";
  const DOWN_AFTER_FAILURES = 2;   // consecutive failures before we stop asking
  const DOWN_COOLDOWN_MS = 5 * 60 * 1000; // re-try after 5 min, in case it was transient
  let consecutiveFailures = 0;

  function isDown() {
    const until = Number(sessionStorage.getItem(DOWN_KEY) || 0);
    return Date.now() < until;
  }

  function noteResult(succeeded) {
    if (succeeded) { consecutiveFailures = 0; return; }
    consecutiveFailures += 1;
    if (consecutiveFailures >= DOWN_AFTER_FAILURES) {
      sessionStorage.setItem(DOWN_KEY, String(Date.now() + DOWN_COOLDOWN_MS));
    }
  }

  // Cache is keyed by caller-supplied key (e.g. phone name + weights, or the
  // exact free-text query) so repeated identical asks reuse a prior answer
  // instead of spending quota on output we already have.
  function cacheGet(key) {
    try { return JSON.parse(sessionStorage.getItem("gm_ai_cache:" + key) || "null"); }
    catch (_) { return null; }
  }
  function cacheSet(key, value) {
    try { sessionStorage.setItem("gm_ai_cache:" + key, JSON.stringify(value)); }
    catch (_) { /* storage full or disabled — degrade to no cache */ }
  }

  return { isDown, noteResult, cacheGet, cacheSet };
})();
