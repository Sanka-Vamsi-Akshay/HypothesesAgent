# main.py
from analysis import adaptive_question_loop
from evaluator import evaluate_problem

def main():
    print("=== AI Hypothesis Generation System ===\n")
    problem = input("Enter your problem: ")

    # Adaptive questioning
    qa_data = adaptive_question_loop(problem)

    # Evaluate and generate conclusion
    print("\n=== FINAL CONCLUSION ===")
    result = evaluate_problem(problem, qa_data)
    print(result)

    # Show Q&A
    print("\n--- Questions & Answers ---")
    for q, a in qa_data:
        print(f"{q} -> {a}")

if __name__ == "__main__":
    main()