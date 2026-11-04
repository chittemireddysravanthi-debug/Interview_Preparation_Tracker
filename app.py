import streamlit as st

from database import create_tables, get_or_create_default_user, get_dashboard_stats

st.set_page_config(
    page_title="Interview Preparation Tracker",
    page_icon="🎯",
    layout="wide",
)

if not create_tables():
    st.error("Could not connect to MySQL. Check database.py settings.")
    st.stop()

if "user_id" not in st.session_state:
    st.session_state.user_id = get_or_create_default_user()

if st.session_state.user_id is None:
    st.error("Could not create or find the default user.")
    st.stop()

st.title("🎯 Interview Preparation Tracker")
st.write(
    "Prepare for interviews, practice questions, take mock interviews, "
    "and track your progress."
)
st.divider()

stats = get_dashboard_stats(st.session_state.user_id)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("📚 Questions", stats["total_questions"])
with c2:
    st.metric("📝 Practice Sessions", stats["practice_sessions"])
with c3:
    st.metric("🎤 Mock Interviews", stats["mock_interviews"])
with c4:
    st.metric("📊 Average Score", f'{stats["average_score"]}%')

st.divider()

st.subheader("🚀 Start Your Preparation")

c1, c2 = st.columns(2)

with c1:
    st.info(
        """### 📝 Practice Questions

Practice Python, SQL, Java, Data Structures, HR and technical questions.

Use the **Practice** page from the sidebar."""
    )

with c2:
    st.info(
        """### 🎤 Mock Interview

Take a mock interview and check your performance and score.

Use the **Mock Interview** page from the sidebar."""
    )

st.subheader("✨ Features")
st.markdown(
    """
- 📊 **Dashboard** — Track preparation progress
- 📚 **Questions** — Manage interview questions
- 📝 **Practice** — Practice questions and save scores
- 🎤 **Mock Interview** — Simulate an interview
- 📈 **Progress** — Monitor topic-wise performance
- 🗄️ **MySQL Database** — Store preparation data
"""
)

st.success("Your Interview Preparation Tracker is ready! 🎉")
