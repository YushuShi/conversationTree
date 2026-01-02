
import os
from google.genai import Client

# Manual .env loading
try:
    with open(".env", "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                key, val = line.strip().split("=", 1)
                os.environ[key] = val.strip('"').strip("'")
except FileNotFoundError:
    try:
        with open("../.env", "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, val = line.strip().split("=", 1)
                    os.environ[key] = val.strip('"').strip("'")
    except FileNotFoundError:
         pass

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Try hardcoded path if needed, or assume it's in env
    print("No API Key found in env, trying to look for .env in current dir")

client = Client(api_key=api_key)

print("Listing models...")
try:
    # Try the method suggested in error or standard list command
    # v1beta often uses client.models.list()
    # But let's check what the SDK supports.
    # The new SDK might be client.models.list()
    
    # We will try to inspect what's available
    
    # Attempt 1: naive list
    for m in client.models.list():
        print(f"Name: {m.name}")
        try:
             # Try new attribute or skip
             methods = getattr(m, "supported_generation_methods", "Unknown")
             print(f"Supported Generation Methods: {methods}")
        except:
             pass
        print("-" * 20)
        
except Exception as e:
    print(f"Error listing models: {e}")

print("\nTesting Generate Content with Gemini 1.5 Flash...")
try:
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Hello, suggest a color."
    )
    print("Success!")
    print(response.text)
except Exception as e:
    print(f"Error generating content: {e}")
