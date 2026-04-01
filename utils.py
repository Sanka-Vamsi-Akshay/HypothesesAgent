# utils.py
import os
import streamlit as st
from groq import Groq

# Use Llama-3.1 8b for fast, free generation
MODEL_NAME = "llama-3.1-8b-instant"

def get_groq_client():
    # Try to get API key from Streamlit secrets (for cloud deployment)
    # Fallback to local environment variable
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = os.environ.get("GROQ_API_KEY")
        
    if not api_key:
        print("Error: GROQ_API_KEY is missing. Please add it to your environment or Streamlit secrets.")
        return None
        
    return Groq(api_key=api_key)

def run_llm(prompt, model=MODEL_NAME):
    """
    Run the Groq cloud model API using the Groq Python SDK.
    """
    client = get_groq_client()
    if not client:
        # Returning a clear error message visible in the UI when they test without a key
        return "Error: GROQ_API_KEY not found. Please set your API key in Streamlit secrets or as an environment variable."
        
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI diagnostic assistant."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
            temperature=0.3,
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error connecting to Groq API: {e}")
        return f"Error connecting to Groq API: {e}"
