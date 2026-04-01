import streamlit as st
from question_agent import generate_initial_questions, generate_followup_questions
from evaluator import evaluate_problem
import string

def normalize(q):
    """Normalize question text for comparison, same as analysis.py."""
    return q.lower().translate(str.maketrans('', '', string.punctuation)).strip()

st.title("🤖 AI Hypothesis Generation & Evaluation System")

# Initialize state machine variables
if "app_state" not in st.session_state:
    st.session_state.app_state = "init"
if "problem" not in st.session_state:
    st.session_state.problem = ""
if "questions" not in st.session_state:
    st.session_state.questions = []
if "all_qa" not in st.session_state:
    st.session_state.all_qa = []
if "asked_questions" not in st.session_state:
    st.session_state.asked_questions = set()
if "round_num" not in st.session_state:
    st.session_state.round_num = 1
if "conclusion" not in st.session_state:
    st.session_state.conclusion = ""

# Helper to restart
def restart():
    for key in ["app_state", "problem", "questions", "all_qa", "asked_questions", "round_num", "conclusion"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# ----------------- STATE: INIT ----------------- #
if st.session_state.app_state == "init":
    st.markdown("Enter your problem below to begin the diagnostic process.")
    
    problem_input = st.text_input("What issue are you facing?", "My phone battery is drying rapidly")
    
    if st.button("Start Analysis"):
        if problem_input.strip():
            st.session_state.problem = problem_input.strip()
            with st.spinner("Generating initial diagnostic questions..."):
                questions = generate_initial_questions(st.session_state.problem)
                st.session_state.questions = questions
                st.session_state.all_qa = []
                st.session_state.asked_questions = {normalize(q) for q in questions}
                st.session_state.round_num = 1
                
                if questions:
                    st.session_state.app_state = "asking"
                else:
                    st.session_state.app_state = "evaluating"
            st.rerun()
        else:
            st.error("Please enter a valid problem to start.")

# ----------------- STATE: ASKING ----------------- #
elif st.session_state.app_state == "asking":
    st.markdown(f"### 🛡️ Diagnostic Round {st.session_state.round_num}")
    st.write(f"**Problem:** {st.session_state.problem}")
    st.markdown("---")
    
    st.write("Please answer the following questions to help us narrow down the issue:")
    answers = []
    
    for i, q in enumerate(st.session_state.questions):
        ans = st.radio(
            label=f"**{i+1}. {q}**",
            options=["yes", "no", "don't know", "other"],
            key=f"q_{st.session_state.round_num}_{i}"
        )
        if ans == "other":
            manual_ans = st.text_input("Please elaborate:", key=f"q_text_{st.session_state.round_num}_{i}")
            answers.append(manual_ans)
        else:
            answers.append(ans)
            
    submit = st.button("Submit Answers")
    
    if submit:
        # Prevent submitting if 'other' is selected but left blank
        if "" in answers:
            st.warning("Please fill out all the 'other' text fields before submitting.")
        else:
            # Store answers
            qa_data = list(zip(st.session_state.questions, answers))
            st.session_state.all_qa.extend(qa_data)
            
            # Request followups based on all accumulated Q&A history
            with st.spinner("Refining hypothesis..."):
                followup_qs = generate_followup_questions(st.session_state.problem, st.session_state.all_qa)
            
            # Filter ones that were already asked
            filtered_followups = []
            for fq in followup_qs:
                norm_fq = normalize(fq)
                if norm_fq not in st.session_state.asked_questions:
                    filtered_followups.append(fq)
                    st.session_state.asked_questions.add(norm_fq)
            
            # Decide transition
            if not filtered_followups or st.session_state.round_num >= 5:
                # We are done asking questions
                st.session_state.app_state = "evaluating"
            else:
                # Move to next round
                st.session_state.questions = filtered_followups
                st.session_state.round_num += 1
                
            st.rerun()

# ----------------- STATE: EVALUATING ----------------- #
elif st.session_state.app_state == "evaluating":
    st.markdown(f"### 🧪 Finalizing Diagnosis")
    with st.spinner("Analyzing all clues and forming the final conclusion..."):
        result = evaluate_problem(st.session_state.problem, st.session_state.all_qa)
        st.session_state.conclusion = result
        st.session_state.app_state = "done"
    st.rerun()

# ----------------- STATE: DONE ----------------- #
elif st.session_state.app_state == "done":
    st.success("Diagnosis Complete!")
    
    st.markdown("### 🏆 Final Conclusion")
    st.info(st.session_state.conclusion)
    
    with st.expander("Show Question & Answer History"):
        for q, a in st.session_state.all_qa:
            st.markdown(f"- **{q}**\n  - *{a}*")
            
    st.markdown("---")
    if st.button("Start New Analysis"):
        restart()