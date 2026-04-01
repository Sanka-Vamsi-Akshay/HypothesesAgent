# question_agent.py
import json
from utils import run_llm

def extract_json(text):
    text = text.strip()
    # Find the first { and last } to strip out markdown backticks or preamble
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        try:
            return json.loads(text[start:end+1])
        except Exception:
            pass
    return None

def generate_initial_questions(problem):
    prompt = f"""
Problem: {problem}

Generate 4-5 completely different diagnostic yes/no/don't know questions to find the root cause.
Output ONLY a valid JSON object in this exact format, with no preamble or markdown formatting:
{{
  "questions": [
    "First question here?",
    "Second question here?"
  ]
}}
"""
    text = run_llm(prompt, json_mode=True)
    data = extract_json(text)
    if data and "questions" in data:
        return data["questions"]
        
    # Fallback parsing just in case
    return [q.strip("- ").strip() for q in text.split("\n") if q.strip() and q.strip().endswith("?")]

def generate_followup_questions(problem, qa_data):
    """
    Generate 2-3 follow-up questions based on previous Q&A.
    If enough information is gathered, stop asking questions.
    """
    prompt = f"""
    You are an expert diagnostician.
Problem: {problem}
Previous Q&A: {qa_data}

Based on the answers thus far, determine if you have gathered enough evidence to form a working hypothesis. 

You MUST respond with ONLY a valid JSON object in this precise format, containing no extra text or markdown:
{{
  "is_done": true or false,
  "questions": [
    "Q1?",
    "Q2?"
  ]
}}

RULES:
1. If you have even a SOLID GUESS or a working hypothesis for the root cause, set "is_done": true and leave the "questions" list empty! We do not want to bore the user with too many questions. Once a good target is identified, stop.
2. If the problem is still entirely mysterious, set "is_done": false and provide 2-3 completely NEW, highly distinct diagnostic questions. Do not repeat previous questions!
"""
    text = run_llm(prompt, json_mode=True)
    data = extract_json(text)
    
    if data is not None:
        if data.get("is_done") is True:
            return [] # We are done!
        return data.get("questions", [])
        
    # Fallback
    if "DONE" in text.upper():
        return []
    return [q.strip("- ").strip() for q in text.split("\n") if q.strip() and q.strip().endswith("?")]
