import os
from dotenv import load_dotenv
from google.genai import types, Client

load_dotenv()

import os
import asyncio
from dotenv import load_dotenv
from google.genai import types, Client

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

async def test():
    try:
        client = Client(api_key=api_key)
        print("Client created.")
        
        # Test Async
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents="Hello",
            config=types.GenerateContentConfig(
                temperature=0.7
            )
        )
        print("Async Response received.")
        print(response.text)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
