import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY") 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Pricing in USD per 1 Million tokens
MODELS = {

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