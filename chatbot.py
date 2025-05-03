from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_response(query: str) -> str:
    """Generate a response to a financial query using OpenAI's Chat API."""
    try:
        model = os.getenv("OPENAI_MODEL", "gpt-4")
        system_prompt = "You are a CFO AI assistant analyzing financial data with columns: Date, Amount, Account, Department."
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"
