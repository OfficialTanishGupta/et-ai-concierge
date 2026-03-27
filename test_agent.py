import os
from dotenv import load_dotenv
load_dotenv(override=True)

api_key = os.getenv("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

from google import genai
import re
import json

client = genai.Client(api_key=api_key)

prompt = 'Return ONLY a JSON array like this: [{"product": "ET Money", "reason": "good for you", "action": "download it", "priority": 1}]'

response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

print("=== RAW RESPONSE ===")
print(response.text)
print("=== END ===")

# Try parsing
json_text = response.text.strip()
json_text = json_text.replace("```json", "").replace("```", "").strip()

match = re.search(r'\[.*\]', json_text, re.DOTALL)
if match:
    json_text = match.group(0)
    print("=== EXTRACTED JSON ===")
    print(json_text)
    parsed = json.loads(json_text)
    print("=== PARSED OK ===")
    print(parsed)
else:
    print("NO JSON ARRAY FOUND")