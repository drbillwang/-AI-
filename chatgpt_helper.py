from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the client with API key from environment variable
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_chatgpt_response(question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": question}
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
    
