from __future__ import annotations
import json
from openai import OpenAI
from .config import OPENAI_API_KEY, OPENAI_MODEL

def judge_delta(old_text: str, new_text: str) -> dict:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY missing — see DIRECTIONS.md")
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = (
        "Compare OLD and NEW page text. Return JSON: "
        '{"material": bool, "score": float 0-1, "summary": string, "changes": [string]}.\n\n'
        f"OLD:\n{old_text[:6000]}\n\nNEW:\n{new_text[:6000]}"
    )
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are ChronoVector Sentinel, a change-detection agent."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        response_format={"type": "json_object"},
    )
    return json.loads(resp.choices[0].message.content or "{}")
