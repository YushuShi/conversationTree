import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    load_dotenv = None

def _load_env_file(path: Path, override: bool) -> bool:
    if load_dotenv is not None:
        load_dotenv(dotenv_path=path, override=override)
        return True

    # Minimal .env parser fallback (KEY=VALUE, supports quotes, ignores comments).
    try:
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if not key:
                continue
            if override or key not in os.environ:
                os.environ[key] = val
        return True
    except Exception:
        return False

def _try_load_dotenv() -> None:
    config_file = Path(__file__).resolve()
    candidate_paths = [
        config_file.parents[2] / ".env",  # conversationTree/.env (your setup)
        config_file.parents[1] / ".env",  # repo root: gemini-alternative-ui/.env
        Path.cwd() / ".env",              # run dir (often reflex_tree/)
    ]
    for path in candidate_paths:
        if path.exists():
            _load_env_file(path, override=True)
            return

_try_load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY") 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SEARCH_API_KEY = os.getenv("TAVILY_API_KEY") or os.getenv("SEARCH_API_KEY")

# Pricing in USD per 1 Million tokens
MODELS = {

    "ChatGPT (GPT-5.2 Pro)": {
        "id": "gpt-5.2-pro",
        "provider": "openai",
        "pricing": {"INPUT_PER_1M": 2.50, "OUTPUT_PER_1M": 10.00}
    },
    "ChatGPT (GPT-5.2)": {
        "id": "gpt-5.2", 
        "provider": "openai",
        "pricing": {"INPUT_PER_1M": 2.50, "OUTPUT_PER_1M": 10.00}
    },
    "ChatGPT (GPT-5 Mini)": {
        "id": "gpt-5-mini", 
        "provider": "openai",
        "pricing": {"INPUT_PER_1M": 0.50, "OUTPUT_PER_1M": 2.00}
    },
    "ChatGPT (GPT-5 Nano)": {
        "id": "gpt-5-nano", 
        "provider": "openai",
        "pricing": {"INPUT_PER_1M": 0.10, "OUTPUT_PER_1M": 0.40}
    },
    "Claude 4.5 Opus": {
        "id": "claude-opus-4-5",
        "provider": "anthropic",
        "pricing": {"INPUT_PER_1M": 15.00, "OUTPUT_PER_1M": 75.00}
    },
    "Claude 4.5 Sonnet": {
        "id": "claude-sonnet-4-5",
        "provider": "anthropic",
        "pricing": {"INPUT_PER_1M": 3.00, "OUTPUT_PER_1M": 15.00}
    },
    "Claude 4.5 Haiku": {
        "id": "claude-haiku-4-5",
        "provider": "anthropic",
        "pricing": {"INPUT_PER_1M": 0.25, "OUTPUT_PER_1M": 1.25}
    },
    "Gemini 2.0 Flash": {
        "id": "gemini-2.0-flash-exp",
        "provider": "google",
        "pricing": {"INPUT_PER_1M": 0.10, "OUTPUT_PER_1M": 0.40}
    },
    "Gemini 3.0 Pro (Preview)": {
        "id": "gemini-3-pro-preview",
        "provider": "google",
        "pricing": {"INPUT_PER_1M": 2.00, "OUTPUT_PER_1M": 12.00}
    }
}

DEFAULT_MODEL_KEY = "ChatGPT (GPT-5.2)"
