"""
Gemini client for the GalaxyMatch AI assistant.

The client is built lazily on first use, so importing this module never
fails. That matters because personas.py and ai_assistant.py import it at
notebook startup: a missing key must degrade to the rule-based fallbacks,
not stop the notebook from opening.
"""

from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_NAME = "gemini-3.5-flash"

# Set GALAXYMATCH_STRICT_AI=1 to make API failures raise instead of falling
# back to templates. Use it for the graded demo: without it a dead API is
# invisible, because every caller treats None as "use the template".
STRICT = os.getenv("GALAXYMATCH_STRICT_AI") == "1"

_client: genai.Client | None = None
_warned_no_key = False


def llm_available() -> bool:
    """True if a key is configured. Does not make a network call."""
    return bool(os.getenv("GEMINI_API_KEY"))


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY not found. Create a .env file with "
                "GEMINI_API_KEY=your-key-here (get one at "
                "https://aistudio.google.com/)."
            )
        _client = genai.Client(api_key=api_key)
    return _client


def call_llm(
    prompt: str,
    expect_json: bool = False,
    config: types.GenerateContentConfig | None = None,
):
    """
    Returns:
        str        -> normal text
        dict       -> parsed JSON
        None       -> any failure (callers fall back to templates)
    """

    try:
        response = _get_client().models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=config,
        )

        # response.text is None when the response is blocked by a safety
        # filter or stops before emitting any text.
        if response.text is None:
            raise ValueError("Gemini returned no text (blocked or empty).")

        text = response.text.strip()

        if not expect_json:
            return text

        return json.loads(text)

    except RuntimeError as e:
        # No key configured. Warn once, then let callers fall back to their
        # rule-based templates so the notebook still runs end to end.
        global _warned_no_key
        if not _warned_no_key:
            _warned_no_key = True
            _report("no API key — using rule-based fallbacks", e)
        elif STRICT:
            raise
        return None

    except json.JSONDecodeError as e:
        _report("JSON parse failed", e, detail=locals().get("text"))
        return None

    except Exception as e:
        _report(type(e).__name__, e)
        return None


def _report(label: str, error: Exception, detail: str | None = None) -> None:
    print("=" * 50)
    print(f"Gemini Error [{label}]:")
    print(error)
    if detail:
        print(f"Raw response: {detail[:200]}")
    print("=" * 50)
    if STRICT:
        raise error
