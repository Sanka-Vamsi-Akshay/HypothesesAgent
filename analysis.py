# analysis.py (final adaptive loop)
from question_agent import generate_initial_questions, generate_followup_questions
import string

def normalize(q):
    """Normalize question text for comparison."""
    return q.lower().translate(str.maketrans('', '', string.punctuation)).strip()

def collect_answers(questions):
    answers = []
    print("\nAnswer with: yes / no / don't know\n")
    for q in questions:
        ans = input(f"{q} (yes/no/don't know): ").strip().lower()
        while ans not in ["yes", "no", "don't know"]:
            ans = input("Please answer yes / no / don't know: ").strip().lower()
        answers.append(ans)
    return answers

def prepare_qa_data(questions, answers):
    return list(zip(questions, answers))

def adaptive_question_loop(problem, max_rounds=5):
    all_qa = []
    asked_questions = set()
    round_num = 1

    print("\nAdaptive question loop starting...")

    # Step 1: initial questions
    questions = generate_initial_questions(problem)

    while questions and round_num <= max_rounds:
        # Normalize and filter questions already asked
        questions = [q for q in questions if normalize(q) not in asked_questions]
        if not questions:
            break  # no new questions, stop loop

        print(f"\n--- Round {round_num} ---")
        answers = collect_answers(questions)
        qa_data = prepare_qa_data(questions, answers)
        all_qa.extend(qa_data)

        # Add normalized questions to asked_questions
        for q in questions:
            asked_questions.add(normalize(q))

        # Generate follow-ups
        questions = generate_followup_questions(problem, all_qa)
        round_num += 1

    return all_qa