"""Temporary stand-in for Member 1's dataset/pipeline and Member 2's engine.

This is Member 3 (UI) scaffolding only — it exists so the notebook can be
built and demoed before the real `data_pipeline.py`/`recommender.py`/
`personas.py`/`badges.py`/`ai_assistant.py` land from teammates. Every
function here matches the exact signature agreed in the team's shared plan,
so swapping a real module in later is a one-line import change in the
notebook, not a rewrite.

Do NOT treat this as the real implementation to build on for Members 1/2/4's
own files — it's intentionally kept separate under `mocks` so their actual
work doesn't collide with this placeholder.
"""

from __future__ import annotations

import re

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# ---------------------------------------------------------------------------
# Mock dataset — matches the official schema exactly:
# model_name, price_inr, ram_gb, storage_gb, camera_mp, battery_mah,
# screen_size_inch, target_segment (gaming/photography/business/budget)
# ---------------------------------------------------------------------------

_RAW_PHONES = [
    # model_name, price_inr, ram_gb, storage_gb, camera_mp, battery_mah, screen_size_inch, target_segment
    ("Galaxy A16", 14999, 4, 128, 50, 5000, 6.7, "budget"),
    ("Galaxy M15", 13999, 4, 128, 50, 6000, 6.5, "budget"),
    ("Galaxy A55", 38999, 8, 128, 50, 5000, 6.6, "business"),
    ("Galaxy A35", 32999, 8, 128, 64, 5000, 6.6, "business"),
    ("Galaxy S23 FE", 49999, 8, 128, 108, 4500, 6.4, "photography"),
    ("Galaxy S24 FE", 59999, 8, 256, 108, 4700, 6.7, "photography"),
    ("Galaxy S24+", 99999, 12, 256, 200, 4900, 6.7, "business"),
    ("Galaxy M55", 26999, 8, 128, 50, 5000, 6.7, "gaming"),
    ("Galaxy F55", 29999, 8, 128, 50, 5000, 6.7, "gaming"),
]

_COLUMNS = [
    "model_name", "price_inr", "ram_gb", "storage_gb",
    "camera_mp", "battery_mah", "screen_size_inch", "target_segment",
]


def mock_phones_df() -> pd.DataFrame:
    """Returns the mock catalogue with camera/performance/battery/value
    scores pre-computed (0-10), as if Member 1's data_pipeline.py already ran."""
    df = pd.DataFrame(_RAW_PHONES, columns=_COLUMNS)

    scaler = MinMaxScaler(feature_range=(0, 10))
    df["camera_score"] = scaler.fit_transform(df[["camera_mp"]])
    df["battery_score"] = scaler.fit_transform(df[["battery_mah"]])

    perf_raw = df["ram_gb"] * 0.6 + df["storage_gb"] * 0.02
    df["performance_score"] = scaler.fit_transform(perf_raw.to_frame())

    quality_avg = df[["camera_score", "performance_score", "battery_score"]].mean(axis=1)
    price_norm = scaler.fit_transform(df[["price_inr"]]).flatten()
    value_raw = quality_avg / (price_norm + 0.1)
    df["value_score"] = scaler.fit_transform(value_raw.to_frame())

    return df


# ---------------------------------------------------------------------------
# Personas — map ~1:1 onto the official target_segment categories
# ---------------------------------------------------------------------------

PERSONAS = {
    "priya": {
        "name": "Priya", "avatar": "P", "age": 24,
        "need": "Wedding photographer — camera & battery first",
        "budget_min": 45000, "budget_max": 70000,
        "weights": {"camera": 0.5, "performance": 0.1, "battery": 0.2, "value": 0.2},
    },
    "arjun": {
        "name": "Arjun", "avatar": "A", "age": 21,
        "need": "Engineering student, BGMI player",
        "budget_min": 20000, "budget_max": 35000,
        "weights": {"camera": 0.1, "performance": 0.5, "battery": 0.3, "value": 0.1},
    },
    "neha": {
        "name": "Neha", "avatar": "N", "age": 29,
        "need": "Consultant, travels weekly",
        "budget_min": 55000, "budget_max": 100000,
        "weights": {"camera": 0.2, "performance": 0.2, "battery": 0.4, "value": 0.2},
    },
    "ravi": {
        "name": "Mr. Ravi", "avatar": "R", "age": 48,
        "need": "Small business owner, keeps it simple",
        "budget_min": 8000, "budget_max": 20000,
        "weights": {"camera": 0.1, "performance": 0.1, "battery": 0.3, "value": 0.5},
    },
}

_BUDGET_MIN, _BUDGET_MAX = 1000, 300000


# ---------------------------------------------------------------------------
# Recommendation engine (mirrors src/recommender.py's future signatures)
# ---------------------------------------------------------------------------

def calculate_score(phone_row: pd.Series, weights: dict) -> float:
    return (
        phone_row["camera_score"] * weights["camera"]
        + phone_row["performance_score"] * weights["performance"]
        + phone_row["battery_score"] * weights["battery"]
        + phone_row["value_score"] * weights["value"]
    )


def recommend_phone(weights: dict, budget_min: float, budget_max: float, df: pd.DataFrame) -> pd.DataFrame:
    scored = df.copy()
    scored["match_score"] = scored.apply(lambda row: calculate_score(row, weights), axis=1)

    in_budget = scored[(scored["price_inr"] >= budget_min) & (scored["price_inr"] <= budget_max)]
    # Widen instead of hard-failing if too few phones fall inside budget.
    result = in_budget if len(in_budget) >= 3 else scored
    return result.sort_values("match_score", ascending=False)


def rank_results(scored_df: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    top = scored_df.head(top_n).copy()
    max_possible = 10.0  # each sub-score is 0-10, weights sum to 1
    top["match_pct"] = (top["match_score"] / max_possible * 100).round().clip(upper=99).astype(int)
    return top


def recommend_all_personas(personas: dict, df: pd.DataFrame) -> dict:
    summary = {}
    for persona_id, persona in personas.items():
        scored = recommend_phone(persona["weights"], persona["budget_min"], persona["budget_max"], df)
        top1 = rank_results(scored, top_n=1)
        summary[persona_id] = top1.iloc[0]
    return summary


def compare_phones(model_names: list, df: pd.DataFrame) -> pd.DataFrame:
    cols = ["model_name", "price_inr", "camera_score", "performance_score", "battery_score", "value_score"]
    return df[df["model_name"].isin(model_names)][cols].set_index("model_name")


# ---------------------------------------------------------------------------
# Badges (mirrors src/badges.py)
# ---------------------------------------------------------------------------

_BADGE_META = {
    "camera_score": ("camera", "Best Camera"),
    "performance_score": ("bolt", "Gaming Beast"),
    "value_score": ("balance", "Best Value"),
    "battery_score": ("bolt", "Marathon Battery"),
}


def assign_badges(df: pd.DataFrame) -> dict:
    badges: dict = {name: [] for name in df["model_name"]}
    for score_col, (icon_name, label) in _BADGE_META.items():
        top_model = df.loc[df[score_col].idxmax(), "model_name"]
        badges[top_model].append((icon_name, label))
    return badges


# ---------------------------------------------------------------------------
# Explanations (mirrors src/ai_assistant.py's template fallback)
# ---------------------------------------------------------------------------

def generate_explanation(weights: dict, phone_row: pd.Series) -> str:
    dominant = max(weights, key=weights.get)
    templates = {
        "camera": f"{phone_row['model_name']}'s camera score leads the shortlist while staying within budget.",
        "performance": f"{phone_row['model_name']} keeps up with demanding use and won't slow down mid-task.",
        "battery": f"{phone_row['model_name']} offers strong all-day battery life for your routine.",
        "value": f"{phone_row['model_name']} gives the best overall spec-for-price balance in range.",
    }
    return templates[dominant]


# ---------------------------------------------------------------------------
# Free-text preference extraction (mirrors src/personas.py's rule-based path)
# ---------------------------------------------------------------------------

_KEYWORD_BUCKETS = {
    "performance": r"bgmi|pubg|gam(e|ing)|fps|fortnite",
    "camera": r"camera|photo|wedding|shoot|photograph",
    "battery": r"travel|consult|client|business trip|meeting|battery",
    "value": r"simple|whatsapp|upi|affordable|small business|budget|calls",
}


def extract_preferences_from_text(description: str) -> dict:
    text = description.lower()
    budget_match = re.search(r"(\d{4,6})", text)
    budget = int(budget_match.group(1)) if budget_match else 40000
    budget_min = max(_BUDGET_MIN, int(budget * 0.7))
    budget_max = min(_BUDGET_MAX, int(budget * 1.15))

    weights = {"camera": 0.2, "performance": 0.2, "battery": 0.3, "value": 0.3}
    for dimension, pattern in _KEYWORD_BUCKETS.items():
        if re.search(pattern, text):
            weights = {k: (0.5 if k == dimension else 0.5 / 3) for k in weights}
            break

    return {"weights": weights, "budget_min": budget_min, "budget_max": budget_max}


def refine_preferences(current_weights: dict, refinement_text: str) -> dict:
    text = refinement_text.lower()
    new_weights = dict(current_weights)
    for dimension, pattern in _KEYWORD_BUCKETS.items():
        if re.search(pattern, text):
            new_weights[dimension] = new_weights.get(dimension, 0.25) + 0.15
    total = sum(new_weights.values())
    return {k: v / total for k, v in new_weights.items()}
