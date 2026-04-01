# evaluator.py
from utils import run_llm

def evaluate_problem(problem, qa_data):
    """
    Generate final conclusion from problem + all Q&A.
    """
    prompt = f"""
Problem: {problem}
Q&A Data: {qa_data}

Analyze the information and provide a final diagnosis.
Do not repeat the questions or the answers. Output ONLY the diagnosis, the underlying cause, and recommendations.
Include a confidence level (LOW, MEDIUM, HIGH) at the end.
IMPORTANT: Do NOT output JSON! Write a beautifully formatted, human-readable markdown response.
"""
    result = run_llm(prompt)
    if not result:
        result = "Failed to generate conclusion."
    return result
