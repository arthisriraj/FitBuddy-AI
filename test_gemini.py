from google import genai
from app.config import GOOGLE_API_KEY

client = genai.Client(api_key=GOOGLE_API_KEY)

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Say hello to FitBuddy in one short sentence."
)

print(response.text)