# question_agent.py
from utils import run_llm

def generate_initial_questions(problem):
    prompt = f"""
Problem: {problem}

Generate 4-5 diagnostic yes/no/don't know questions.
List each question on a new line, no explanations.
"""
    text = run_llm(prompt)
    questions = [q.strip("- ").strip() for q in text.split("\n") if q.strip() and q.strip().endswith("?")]
    return questions

def generate_followup_questions(problem, qa_data):
    """
    Generate 2-3 follow-up questions based on previous Q&A.
    If enough information is gathered, stop asking questions.
    """
    prompt = f"""
Problem: {problem}
Previous Q&A: {qa_data}

Based on the answers, if you have gathered enough definitive evidence to pinpoint the EXACT root cause with HIGH confidence, you MUST respond with the single word "DONE" and nothing else.
If you do NOT know the exact root cause yet, generate 2-3 new, completely different diagnostic yes/no/don't know questions to narrow down the problem. Do NOT output the word "DONE" anywhere in your response if you are asking questions. List each question on a new line.
"""
    text = run_llm(prompt).strip()
    if "DONE" in text.upper():
        return []
        
    questions = [q.strip("- ").strip() for q in text.split("\n") if q.strip() and q.strip().endswith("?")]
    return questions
