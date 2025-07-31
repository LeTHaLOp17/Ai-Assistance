# ai_client.py
# Interface with AI models: Google Gemini (active) and OpenAI (commented out)

import google.generativeai as genai
from config import GEMINI_API_KEY

# Configure Gemini API client
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

def get_ai_response(user_input: str) -> str:
    """
    Get AI response from Google Gemini.
    """
    system_prompt = "You are luffy, a helpful, friendly AI assistant."
    prompt_text = f"{system_prompt}\nUser: {user_input}\nAssistant:"
    response = gemini_model.generate_content(
        prompt_text,
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.9
        }
    )
    return response.text.strip()

"""
# OpenAI API integration (commented out for now)

import openai
from config import OPENAI_API_KEY

openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

def get_openai_response(user_input: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful, friendly AI assistant."},
        {"role": "user", "content": user_input}
    ]
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.strip()
"""
