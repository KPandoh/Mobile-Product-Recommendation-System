"""4 personas + free-text preference extraction (Step 2 / Step 2b of the plan).

Personas map ~1:1 onto real shopper types:
Riya->photography, Kabir->gaming, Ananya->business, Mukesh->budget.

Weights cover five dimensions (camera / performance / battery / display /
value) and always sum to 1.0.
"""

from __future__ import annotations

import re

from src import llm_client, security
from src.prompts import PERSONA_PROMPT

PERSONAS = {
    "riya": {
        "name": "Riya Sharma",
        "avatar": "R",
        "age": 26,
        "need": "Travel content creator who captures photos and Instagram reels. Prioritizes camera quality and dependable battery life.",
        "budget_min": 45000,
        "budget_max": 70000,
        "weights": {
            "camera": 0.40,
            "performance": 0.08,
            "battery": 0.16,
            "display": 0.20,
            "value": 0.16,
        },
    },

    "kabir": {
        "name": "Kabir Mehta",
        "avatar": "K",
        "age": 22,
        "need": "Computer Science student and mobile gaming enthusiast. Plays BGMI, COD Mobile and multitasks between studies and entertainment.",
        "budget_min": 22000,
        "budget_max": 38000,
        "weights": {
            "camera": 0.08,
            "performance": 0.40,
            "battery": 0.24,
            "display": 0.20,
            "value": 0.08,
        },
    },

    "ananya": {
        "name": "Ananya Rao",
        "avatar": "A",
        "age": 31,
        "need": "Management consultant who frequently travels for client meetings. Needs reliable battery life, smooth multitasking and a premium experience.",
        "budget_min": 55000,
        "budget_max": 95000,
        "weights": {
            "camera": 0.16,
            "performance": 0.16,
            "battery": 0.32,
            "display": 0.20,
            "value": 0.16,
        },
    },

    "mukesh": {
        "name": "Mukesh Patel",
        "avatar": "M",
        "age": 47,
        "need": "Owns a neighbourhood grocery store. Uses WhatsApp Business, UPI payments, YouTube and video calls. Wants maximum value for money and long battery life.",
        "budget_min": 12000,
        "budget_max": 22000,
        "weights": {
            "camera": 0.09,
            "performance": 0.09,
            "battery": 0.27,
            "display": 0.10,
            "value": 0.45,
        },
    },
}

_KEYWORD_BUCKETS = {
    "performance": r"bgmi|pubg|gaming|gamer|fps|fortnite|cod|call of duty|genshin|esports",
    "camera": r"camera|photo|photography|reels|instagram|content creator|shoot|video|vlog",
    "battery": r"travel|travelling|consultant|meeting|office|battery|remote work|work",
    "display": r"screen|display|amoled|refresh rate|watch(ing)? (video|movie)|streaming|binge",
    "value": r"budget|value|upi|whatsapp|shop|business|affordable|daily use|student",
}

_rate_limiter = security.RateLimiter()


def _extract_rule_based(description: str) -> dict:
    text = description.lower()
    budget_match = re.search(r"(\d{4,6})", text)
    budget = int(budget_match.group(1)) if budget_match else 40000
    budget_min = security.clamp_budget(budget * 0.7)
    budget_max = security.clamp_budget(budget * 1.15)

    weights = {"camera": 0.15, "performance": 0.2, "battery": 0.25, "display": 0.15, "value": 0.25}
    for dimension, pattern in _KEYWORD_BUCKETS.items():
        if re.search(pattern, text):
            weights = {k: (0.5 if k == dimension else 0.5 / 4) for k in weights}
            break

    return {"weights": weights, "budget_min": budget_min, "budget_max": budget_max}


def call_llm_extract(description: str) -> dict | None:
    """Uses Gemini to extract preferences from natural language."""

    if not _rate_limiter.allow():
        return None

    prompt = (
        PERSONA_PROMPT
        + "\n\nCustomer Description:\n"
        + description
    )

    result = llm_client.call_llm(
        prompt,
        expect_json=True,
    )

    if not result:
        return None

    try:
        weights = {
            "camera": result["camera"],
            "performance": result["performance"],
            "battery": result["battery"],
            # display was added as a 5th dimension; default keeps us tolerant
            # of model outputs that omit it.
            "display": result.get("display", 2),
            "value": result["value"],
        }

        total = sum(weights.values())

        if total == 0:
            return None

        weights = {
            key: value / total
            for key, value in weights.items()
        }

        budget = security.clamp_budget(result["budget"])

        return {
            "weights": weights,
            "budget_min": security.clamp_budget(int(budget * 0.8)),
            "budget_max": security.clamp_budget(int(budget * 1.2)),
        }

    except (KeyError, TypeError):
        return None


def extract_preferences_from_text(description: str) -> dict:
    return call_llm_extract(description) or _extract_rule_based(description)


def refine_preferences(current_weights: dict, refinement_text: str) -> dict:
    text = refinement_text.lower()
    new_weights = dict(current_weights)
    for dimension, pattern in _KEYWORD_BUCKETS.items():
        if re.search(pattern, text):
            new_weights[dimension] = new_weights.get(dimension, 0.25) + 0.15
    total = sum(new_weights.values())
    return {k: v / total for k, v in new_weights.items()}
