
import random
import streamlit as st

from database import (
    add_practice_session,
    add_progress,
    get_questions,
)

st.set_page_config(
    page_title="Practice",
    page_icon="📝",
    layout="wide",
)

st.title("📝 Interview Practice")
st.write("Answer technical and HR interview questions and track your performance.")

# Check user login
if "user_id" not in st.session_state:
    st.error("Please open the Dashboard first.")
    st.stop()

# Initialize practice session
if "practice_started" not in st.session_state:
    st.session_state.practice_started = False

# Select category
categories = [
    "All",
    "Python",
    "SQL",
    "Java",
    "Data Structures",
    "HR",
    "AIML",
]

category = st.selectbox("Select Category", categories)

all_questions = get_questions(category)

if not all_questions:
    st.warning("No questions available in this category.")
    st.info("Go to the Questions page and add questions with their answers.")
    st.stop()

# Select number of questions
max_questions = len(all_questions)

number_of_questions = st.slider(
    "Number of Questions",
    min_value=1,
    max_value=max_questions,
    value=min(5, max_questions),
)

# Start practice
if st.button("🚀 Start Practice", type="primary"):
    selected = random.sample(
        all_questions,
        min(number_of_questions, len(all_questions)),
    )

    st.session_state.practice_questions = selected
    st.session_state.practice_category = category
    st.session_state.practice_started = True
    st.session_state.practice_phase = "answer"

    st.rerun()


# Display questions
if st.session_state.practice_started:

    questions = st.session_state.practice_questions

    st.divider()

    # PHASE 1: Answer questions
    if st.session_state.practice_phase == "answer":

        st.subheader("📝 Answer the Interview Questions")

        st.info(
            "Write your own answer for every question. "
            "Submit your answers to view the expected answers."
        )

        for index, q in enumerate(questions):

            st.markdown(f"### Question {index + 1}")
            st.write(q["question"])

            st.text_area(
                "Your Answer",
                key=f"user_answer_{q['id']}",
                height=120,
                placeholder="Type your interview answer here...",
            )

            st.divider()

        if st.button("📤 Submit Answers", type="primary"):

            unanswered = [
                q for q in questions
                if not st.session_state.get(
                    f"user_answer_{q['id']}", ""
                ).strip()
            ]

            if unanswered:
                st.warning("Please answer all questions before submitting.")
            else:
                st.session_state.practice_phase = "review"
                st.rerun()

    # PHASE 2: Review answers
    elif st.session_state.practice_phase == "review":

        st.subheader("📖 Review Your Answers")

        st.info(
            "Compare your response with the expected answer "
            "and select whether your answer is correct."
        )

        for index, q in enumerate(questions):

            st.markdown(f"### Question {index + 1}")

            st.write(q["question"])

            st.markdown("**Your Answer:**")
            st.write(
                st.session_state.get(
                    f"user_answer_{q['id']}", ""
                )
            )

            st.markdown("**Expected Answer:**")

            expected_answer = q.get("answer")

            if expected_answer:
                st.success(expected_answer)
            else:
                st.warning(
                    "Expected answer is not available. "
                    "Please add an answer on the Questions page."
                )

            st.radio(
                "Evaluate your answer",
                ["Select...", "Correct", "Incorrect"],
                index=0,
                key=f"rating_{q['id']}",
            )

            st.divider()

        if st.button("✅ Finish Practice", type="primary"):

            ratings = [
                st.session_state.get(f"rating_{q['id']}")
                for q in questions
            ]

            if any(rating == "Select..." for rating in ratings):
                st.warning("Please evaluate all your answers.")
            else:

                correct = sum(
                    1 for rating in ratings
                    if rating == "Correct"
                )

                attempted = len(questions)

                score = round(
                    (correct / attempted) * 100, 2
                )

                saved = add_practice_session(
                    st.session_state.user_id,
                    st.session_state.practice_category,
                    attempted,
                    correct,
                    score,
                )

                if saved:

                    if st.session_state.practice_category != "All":
                        add_progress(
                            st.session_state.user_id,
                            st.session_state.practice_category,
                            attempted,
                            correct,
                            score,
                        )

                    st.session_state.practice_started = False
                    st.session_state.practice_phase = "completed"

                    st.success("🎉 Practice Completed Successfully!")

                    c1, c2, c3 = st.columns(3)

                    with c1:
                        st.metric("Total Questions", attempted)

                    with c2:
                        st.metric("Correct Answers", correct)

                    with c3:
                        st.metric("Your Score", f"{score}%")

                    if score >= 80:
                        st.balloons()
                        st.success("Excellent performance! Keep it up.")
                    elif score >= 50:
                        st.info("Good effort! Keep practicing.")
                    else:
                        st.warning("Keep learning and try again.")

                else:
                    st.error("Could not save your practice session.")
