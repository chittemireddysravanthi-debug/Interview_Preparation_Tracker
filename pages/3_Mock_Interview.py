
import random
import streamlit as st

from database import add_mock_interview, get_questions

st.set_page_config(
    page_title="Mock Interview",
    page_icon="🎤",
    layout="wide",
)

st.title("🎤 Mock Interview")
st.write("Practice interview questions and evaluate your performance.")

if "user_id" not in st.session_state:
    st.error("Please open the Dashboard first.")
    st.stop()

# Interview type
interview_type = st.selectbox(
    "Select Interview Type",
    ["Technical", "HR", "Python", "SQL", "AIML"],
)

# Get questions
questions = get_questions(
    None if interview_type in ["Technical", "HR"] else interview_type
)

if not questions:
    st.warning("No questions available for this interview type.")
    st.info("Please add questions from the Questions page first.")
    st.stop()

# Number of questions
number_of_questions = st.slider(
    "Number of questions",
    min_value=1,
    max_value=len(questions),
    value=min(5, len(questions)),
)

# Start interview
if st.button("🎤 Start Mock Interview"):
    st.session_state.mock_questions = random.sample(
        questions, number_of_questions
    )
    st.session_state.mock_started = True
    st.session_state.mock_type = interview_type
    st.session_state.mock_submitted = False
    st.rerun()

# Interview section
if st.session_state.get("mock_started", False):

    selected = st.session_state.mock_questions

    st.divider()
    st.subheader("📝 Interview Questions")

    with st.form("mock_interview_form"):

        answers = {}

        for i, q in enumerate(selected, start=1):

            st.markdown(f"### Question {i}")
            st.write(q["question"])

            answers[q["id"]] = st.text_area(
                "Your Answer",
                key=f"answer_{q['id']}",
                placeholder="Type your answer here...",
                height=120,
            )

        feedback = st.text_area(
            "Additional Notes",
            placeholder="Write your interview experience or notes...",
        )

        submitted = st.form_submit_button(
            "💾 Submit Mock Interview"
        )

    if submitted:

        attempted = len(selected)
        answered = sum(
            1 for answer in answers.values() if answer.strip()
        )

        score = round((answered / attempted) * 100, 2)

        st.session_state.mock_answers = answers
        st.session_state.mock_feedback = feedback
        st.session_state.mock_attempted = attempted
        st.session_state.mock_answered = answered
        st.session_state.mock_score = score

        st.session_state.mock_submitted = True
        st.rerun()

# Results section
if st.session_state.get("mock_submitted", False):

    st.divider()
    st.subheader("📊 Interview Results")

    attempted = st.session_state.mock_attempted
    answered = st.session_state.mock_answered
    score = st.session_state.mock_score

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Questions", attempted)
    col2.metric("Answered", answered)
    col3.metric("Completion Score", f"{score}%")

    st.info(
        "This score measures answer completion only. "
        "It does not automatically evaluate answer correctness."
    )

    if st.button("💾 Save Interview Results"):

        saved = add_mock_interview(
            st.session_state.user_id,
            st.session_state.mock_type,
            attempted,
            answered,
            score,
            st.session_state.mock_feedback,
        )

        if saved:
            st.success("Mock interview results saved successfully!")

            st.session_state.mock_started = False
            st.session_state.mock_submitted = False

        else:
            st.error("Could not save the mock interview.")

    if st.button("🔄 Start Another Interview"):
        st.session_state.mock_started = False
        st.session_state.mock_submitted = False
        st.rerun()
