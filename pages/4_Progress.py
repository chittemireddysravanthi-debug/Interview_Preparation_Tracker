import pandas as pd
import streamlit as st

from database import get_dashboard_stats, get_progress, get_practice_sessions, get_mock_interviews

st.set_page_config(page_title="Progress", page_icon="📈", layout="wide")

st.title("📈 Progress Tracking")

if "user_id" not in st.session_state:
    st.error("Please open the Dashboard first.")
    st.stop()

stats = get_dashboard_stats(st.session_state.user_id)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Practice Sessions", stats["practice_sessions"])
with c2:
    st.metric("Mock Interviews", stats["mock_interviews"])
with c3:
    st.metric("Average Practice Score", f'{stats["average_score"]}%')

st.divider()

st.subheader("📚 Topic Progress")
progress = get_progress(st.session_state.user_id)

if progress:
    df = pd.DataFrame(progress)
    st.dataframe(
        df[
            [
                "topic",
                "completed_questions",
                "correct_answers",
                "score",
                "updated_at",
            ]
        ],
        use_container_width=True,
    )
else:
    st.info("No topic progress recorded yet.")

st.subheader("📝 Practice History")
practice = get_practice_sessions(st.session_state.user_id)

if practice:
    df = pd.DataFrame(practice)
    st.dataframe(
        df[
            [
                "category",
                "questions_attempted",
                "questions_correct",
                "score",
                "session_date",
            ]
        ],
        use_container_width=True,
    )
else:
    st.info("No practice sessions yet.")

st.subheader("🎤 Mock Interview History")
mocks = get_mock_interviews(st.session_state.user_id)

if mocks:
    df = pd.DataFrame(mocks)
    st.dataframe(
        df[
            [
                "interview_type",
                "questions_attempted",
                "questions_correct",
                "score",
                "feedback",
                "interview_date",
            ]
        ],
        use_container_width=True,
    )
else:
    st.info("No mock interviews yet.")
