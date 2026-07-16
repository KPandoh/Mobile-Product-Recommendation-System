"""
Explanation generation (Step 7 of the plan)

Enhanced Version

Features
--------
✔ Gemini AI support
✔ Rule-based fallback
✔ Uses persona priorities
✔ Uses phone strengths
✔ Human-friendly explanations
✔ Safe HTML output
"""

from __future__ import annotations

import pandas as pd

from src import llm_client, security
from src.prompts import (
    EXPLANATION_PROMPT,
    BADGE_PROMPT,
    COMPARISON_PROMPT,
    SUMMARY_PROMPT,
)

_rate_limiter = security.RateLimiter()


# ---------------------------------------------------------
# RULE-BASED EXPLANATIONS
# ---------------------------------------------------------

def _strongest_feature(phone_row: pd.Series) -> tuple[str, float]:
    features = {
        "camera": phone_row["camera_score"],
        "performance": phone_row["performance_score"],
        "battery": phone_row["battery_score"],
        "value": phone_row["value_score"],
    }

    feature = max(features, key=features.get)

    return feature, features[feature]


def _generate_template(weights: dict, phone_row: pd.Series) -> str:

    dominant_priority = max(weights, key=weights.get)

    strongest_feature, feature_score = _strongest_feature(phone_row)

    model = phone_row["model_name"]

    # Ideal case
    if dominant_priority == strongest_feature:

        templates = {
            "camera":
                f"{model} is an excellent choice because its outstanding camera quality perfectly matches your photography priorities.",

            "performance":
                f"{model} delivers powerful performance that makes gaming and multitasking smooth and responsive.",

            "battery":
                f"{model} offers impressive battery life, making it ideal for long workdays and travel.",

            "value":
                f"{model} provides excellent value for money while delivering balanced overall performance.",
        }

        return templates[dominant_priority]

    # Mixed strengths

    return (
        f"{model} provides a balanced combination of "
        f"{strongest_feature} performance while still aligning well "
        f"with your personal preferences."
    )


# ---------------------------------------------------------
# LLM EXPLANATION
# ---------------------------------------------------------

def generate_explanation_llm(
    weights: dict,
    phone_row: pd.Series,
) -> str | None:

    if not _rate_limiter.allow():
        return None

    # Calculate an overall score for the prompt
    overall_score = round(
        (
            phone_row["camera_score"]
            + phone_row["performance_score"]
            + phone_row["battery_score"]
            + phone_row["value_score"]
        ) / 4,
        1,
    )

    prompt = EXPLANATION_PROMPT.format(
        persona=(
            f"Camera Priority: {weights['camera']}, "
            f"Performance Priority: {weights['performance']}, "
            f"Battery Priority: {weights['battery']}, "
            f"Value Priority: {weights['value']}"
        ),
        phone=phone_row["model_name"],
        camera=f"{phone_row['camera_score']:.1f}",
        performance=f"{phone_row['performance_score']:.1f}",
        battery=f"{phone_row['battery_score']:.1f}",
        value=f"{phone_row['value_score']:.1f}",
        overall=overall_score,
    )

    return llm_client.call_llm(
        prompt,
        expect_json=False,
    )


# ---------------------------------------------------------
# PUBLIC FUNCTION
# ---------------------------------------------------------

def generate_explanation(
    weights: dict,
    phone_row: pd.Series,
) -> str:

    explanation = generate_explanation_llm(
        weights,
        phone_row,
    )

    if not explanation:

        explanation = _generate_template(
            weights,
            phone_row,
        )

    return security.sanitize_for_html(explanation)




def generate_badge_reason(phone_row, badge):

    prompt = BADGE_PROMPT.format(
        phone=phone_row["model_name"],
        camera=phone_row["camera_score"],
        performance=phone_row["performance_score"],
        battery=phone_row["battery_score"],
        value=phone_row["value_score"],
    )

    reason = llm_client.call_llm(
        prompt,
        expect_json=False,
    )

    if reason:
        return reason

    fallback = {
        "🏆 Best Camera":
            "Outstanding camera capabilities make this phone ideal for photography.",

        "🎮 Gaming Beast":
            "High performance delivers a smooth gaming and multitasking experience.",

        "🔋 Battery Champion":
            "Long-lasting battery makes it suitable for heavy daily use.",

        "💰 Best Value":
            "Excellent balance between price and overall performance.",
    }

    return fallback.get(
        badge,
        "A well-balanced Samsung smartphone."
    )

def compare_phones_ai(phone1, phone2):
    """
    Generates an AI comparison between two phones.
    Falls back to a rule-based comparison if Gemini
    is unavailable.
    """

    prompt = COMPARISON_PROMPT.format(
        phone1=phone1["model_name"],
        camera1=phone1["camera_score"],
        performance1=phone1["performance_score"],
        battery1=phone1["battery_score"],
        value1=phone1["value_score"],
        phone2=phone2["model_name"],
        camera2=phone2["camera_score"],
        performance2=phone2["performance_score"],
        battery2=phone2["battery_score"],
        value2=phone2["value_score"],
    )

    comparison = llm_client.call_llm(
        prompt,
        expect_json=False,
    )

    if comparison:
        return comparison

    # ---------- Rule-based fallback ----------

    winner = []

    for feature in [
        "camera_score",
        "performance_score",
        "battery_score",
        "value_score",
    ]:

        if phone1[feature] > phone2[feature]:
            winner.append(
                f"{phone1['model_name']} has better {feature.replace('_score','')}."
            )

        elif phone2[feature] > phone1[feature]:
            winner.append(
                f"{phone2['model_name']} has better {feature.replace('_score','')}."
            )

    return " ".join(winner)

def generate_recommendation_summary(weights, top_phones):
    """
    Generates an AI summary for the top recommended phones.
    Falls back to a rule-based summary if Gemini is unavailable.
    """

    prompt = SUMMARY_PROMPT.format(
        priorities=(
            f"Camera: {weights['camera']}, "
            f"Performance: {weights['performance']}, "
            f"Battery: {weights['battery']}, "
            f"Value: {weights['value']}"
        ),
        phone1=top_phones[0]["model_name"],
        phone2=top_phones[1]["model_name"],
        phone3=top_phones[2]["model_name"],
    )

    summary = llm_client.call_llm(
        prompt,
        expect_json=False,
    )

    if summary:
        return security.sanitize_for_html(summary)

    return (
        f"Based on your preferences, "
        f"{top_phones[0]['model_name']} is the strongest recommendation. "
        f"{top_phones[1]['model_name']} is an excellent alternative, while "
        f"{top_phones[2]['model_name']} offers another balanced Samsung option."
    )



    