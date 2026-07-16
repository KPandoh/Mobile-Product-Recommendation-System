from __future__ import annotations

import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found. Please create a .env file."
    )

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.5-flash"


def call_llm(
    prompt: str,
    expect_json: bool = False,
):
    """
    Returns:
        str        -> normal text
        dict       -> parsed JSON
        None       -> any failure
    """

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )

        text = response.text.strip()

        if not expect_json:
            return text

        return json.loads(text)

    except Exception as e:
        print("=" * 50)
        print("Gemini Error:")
        print(e)
        print("=" * 50)
        return None