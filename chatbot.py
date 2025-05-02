import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_response(query: str) -> str:
    """Generate a response to a financial query using OpenAI's GPT-4."""
    try:
        response = openai.Completion.create(
            model="gpt-4",
            prompt=query,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"
