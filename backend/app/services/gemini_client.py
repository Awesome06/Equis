from google import genai
from google.genai import types
from app.config import settings
from typing import List, Dict
import json

# Initialize Gemini client
client = genai.Client(api_key=settings.GEMINI_API_KEY)

async def categorize_transactions(descriptions: List[str]) -> List[Dict[str, str]]:
    """
    Uses Gemini API to categorize a list of bank transaction descriptions.
    Returns a list of dictionaries with 'description' and 'category'.
    """
    if not descriptions:
        return []

    prompt = f"""
    You are a financial data expert. Categorize the following bank transaction descriptions into exactly one of these categories:
    Rent, Utilities, Income, Discretionary, or Unclassified.

    Respond ONLY with a valid JSON array of objects, where each object has "description" and "category" keys.
    
    Transactions:
    {json.dumps(descriptions)}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        
        # Parse the response text as JSON
        results = json.loads(response.text)
        return results
    except Exception as e:
        print(f"Gemini API Error: {str(e)}")
        # Return unclassified for everything if Gemini fails
        return [{"description": d, "category": "Unclassified"} for d in descriptions]
