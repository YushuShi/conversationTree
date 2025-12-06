import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Pricing in USD per 1 Million tokens
MODELS = {
    "Gemini 3.0 Pro (Preview)": {
        "id": "gemini-3-pro-preview",
        "pricing": {"INPUT_PER_1M": 2.00, "OUTPUT_PER_1M": 12.00}
    },
    "Gemini 2.0 Flash": {
        "id": "gemini-2.0-flash",
        "pricing": {"INPUT_PER_1M": 0.10, "OUTPUT_PER_1M": 0.40}
    },
    "Gemini 1.5 Pro": {
        "id": "gemini-1.5-pro",
        "pricing": {"INPUT_PER_1M": 3.50, "OUTPUT_PER_1M": 10.50}
    },
    "Gemini 1.5 Flash": {
        "id": "gemini-1.5-flash",
        "pricing": {"INPUT_PER_1M": 0.075, "OUTPUT_PER_1M": 0.30}
    }
}

DEFAULT_MODEL_KEY = "Gemini 2.0 Flash"