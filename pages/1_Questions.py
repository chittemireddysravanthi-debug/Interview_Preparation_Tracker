import streamlit as st
from database import add_question, get_questions

st.set_page_config(page_title="Questions", page_icon="📚", layout="wide")

st.title("📚 Interview Questions")
st.write("Add and view interview questions.")

with st.expander("➕ Add New Question", expanded=True):
    with st.form("question_form"):
        question = st.text_area("Question")
        category = st.selectbox(
            "Category",
            ["Python", "SQL", "Java", "Data Structures", "HR", "AIML"],
        )
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        answer = st.text_area("Answer / Explanation")

        submitted = st.form_submit_button("Add Question")

        if submitted:
            if not question.strip():
                st.warning("Please enter a question.")
            else:
                if add_question(
                    question.strip(),
                    category,
                    difficulty,
                    answer.strip(),
                ):
                    st.success("Question added successfully!")
                    st.rerun()
                else:
                    st.error("Could not add question.")

st.divider()

st.subheader("📖 Question Bank")

category_filter = st.selectbox(
    "Filter by Category",
    ["All", "Python", "SQL", "Java", "Data Structures", "HR", "AIML"],
)

questions = get_questions(category_filter)

if not questions:
    st.info("No questions found. Add your first question above.")
else:
    for i, q in enumerate(questions, start=1):
        with st.expander(
            f"{i}. {q['question']} — {q['category']} ({q['difficulty']})"
        ):
            st.write("**Category:**", q["category"])
            st.write("**Difficulty:**", q["difficulty"])
            if q["answer"]:
                st.write("**Answer:**")
                st.write(q["answer"])
