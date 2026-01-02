# Conversation Tree (Reflex Version)

## Prerequisites
- Python 3.9+
- NodeJS 16+ (install from https://nodejs.org or via Homebrew: `brew install node`)
- Reflex (`pip install reflex`)

## How to Run

1. Install Python dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

## Environment Variables

- `OPENAI_API_KEY` (for OpenAI models)
- `ANTHROPIC_API_KEY` (for Claude models)
- `GEMINI_API_KEY` (for Gemini models)
- `TAVILY_API_KEY` (optional; enables “Deep Search” web grounding for OpenAI/Gemini/Anthropic)

## Usage Tracking

- Session, daily, weekly, and overall usage (cost + tokens) is tracked per user.
- Use the “API Settings” dialog to store provider keys (including Tavily) per account.

2. Initialize (first time only, already done):
   ```bash
   reflex init
   ```

3. Run the application:
   ```bash
   reflex run
   ```

4. Open your browser:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: http://localhost:8000
