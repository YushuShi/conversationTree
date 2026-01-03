import os
import sys

import anthropic
import openai
from google.genai import Client, types

from reflex_tree import config


def test_openai(model_id: str) -> str:
    key = os.getenv("OPENAI_API_KEY", "")
    if not key:
        return "skip (missing OPENAI_API_KEY)"
    client = openai.OpenAI(api_key=key)
    response = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": "ping"}],
    )
    content = response.choices[0].message.content
    return "ok" if content else "fail (empty response)"


def test_anthropic(model_id: str) -> str:
    key = os.getenv("ANTHROPIC_API_KEY", "")
    if not key:
        return "skip (missing ANTHROPIC_API_KEY)"
    client = anthropic.Anthropic(api_key=key)
    response = client.messages.create(
        model=model_id,
        max_tokens=32,
        temperature=0.7,
        messages=[{"role": "user", "content": "ping"}],
        system="You are a helpful assistant.",
    )
    content = response.content[0].text if response.content else ""
    return "ok" if content else "fail (empty response)"


def test_google(model_id: str) -> str:
    key = os.getenv("GEMINI_API_KEY", "")
    if not key:
        return "skip (missing GEMINI_API_KEY)"
    client = Client(api_key=key)
    response = client.models.generate_content(
        model=model_id,
        contents=[
            types.Content(
                role="user",
                parts=[types.Part.from_text(text="ping")],
            )
        ],
        config=types.GenerateContentConfig(temperature=0.7),
    )
    content = getattr(response, "text", "") or ""
    return "ok" if content else "fail (empty response)"


def main() -> int:
    tests = {
        "openai": test_openai,
        "anthropic": test_anthropic,
        "google": test_google,
    }
    failures = 0
    for name, info in config.MODELS.items():
        provider = info.get("provider")
        model_id = info.get("id")
        tester = tests.get(provider)
        if not tester:
            print(f"{name}: fail (unknown provider {provider})")
            failures += 1
            continue
        try:
            result = tester(model_id)
        except Exception as exc:
            result = f"fail ({exc})"
        print(f"{name}: {result}")
        if result.startswith("fail"):
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
