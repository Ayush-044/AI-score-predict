import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ==================================
# PAGE CONFIG (MUST BE FIRST)
# ==================================
st.set_page_config(
    page_title="AI Exam Score Predictor",
    page_icon="🧠",
    layout="wide"
)

BACKEND_URL = "http://127.0.0.1:8000"

# ==================================
# SESSION STATE INIT
# ==================================
if "student_logged_in" not in st.session_state:
    st.session_state.student_logged_in = False
    st.session_state.student_name = None

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post(f"{BACKEND_URL}/student/login", json={"username": username, "password": password})
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                st.error(data["error"])
            # Handling a subtle bug seen in backend for the error key having space
            elif "error " in data:
                st.error(data["error "])
            else:
                st.success(data["message"])
                st.session_state.student_logged_in = True
                st.session_state.student_name = data["username"]
                st.rerun()
        else:
            st.error("Login failed")

def register():
    st.subheader("Register")
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    if st.button("Register"):
        response = requests.post(f"{BACKEND_URL}/student/register", json={"username": username, "password": password})
        if response.status_code == 200:
            data = response.json()
            if "error" in data:
                st.error(data["error"])
            else:
                st.success(data["message"])
                st.info("Registration successful. You can now login in the Login tab.")
        else:
            st.error("Registration failed")

def predict_score():
    st.subheader("Predict Exam Score")
    with st.form("predict_form"):
        st.write(f"Student Information for: **{st.session_state.student_name}**")
        
        col1, col2 = st.columns(2)
        with col1:
            hours_studied = st.number_input("Hours Studied (0-24)", min_value=0, max_value=24, value=5)
            attendance = st.number_input("Attendance % (0-100)", min_value=0, max_value=100, value=80)
            parental_involvement = st.selectbox("Parental Involvement", ["Low", "Medium", "High"])
            access_to_resources = st.selectbox("Access to Resources", ["Low", "Medium", "High"])
            sleep_hours = st.number_input("Sleep Hours (0-24)", min_value=0, max_value=24, value=7)
            previous_scores = st.number_input("Previous Scores % (0-100)", min_value=0, max_value=100, value=75)
            internet_access = st.selectbox("Internet Access", ["Yes", "No"])
        with col2:
            motivation_level = st.selectbox("Motivation Level", ["Low", "Medium", "High"])
            tutoring_sessions = st.number_input("Tutoring Sessions (0-100)", min_value=0, max_value=100, value=0)
            family_income = st.selectbox("Family Income", ["Low", "Medium", "High"])
            teacher_quality = st.selectbox("Teacher Quality", ["Low", "Medium", "High"])
            peer_influence = st.selectbox("Peer Influence", ["Positive", "Negative", "Neutral"])
            parental_education = st.selectbox("Parental Education Level", ["High School", "College", "Postgraduate"])

        submitted = st.form_submit_button("Predict Score")
        if submitted:
            payload = {
                "name": st.session_state.student_name,
                "Hours_Studied": hours_studied,
                "Attendance": attendance,
                "Parental_Involvement": parental_involvement,
                "Access_to_Resources": access_to_resources,
                "Sleep_Hours": sleep_hours,
                "Previous_Scores": previous_scores,
                "Motivation_Level": motivation_level,
                "Internet_Access": internet_access,
                "Tutoring_Sessions": tutoring_sessions,
                "Family_Income": family_income,
                "Teacher_Quality": teacher_quality,
                "Peer_Influence": peer_influence,
                "Parental_Education_Level": parental_education
            }
            try:
                response = requests.post(f"{BACKEND_URL}/predict", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"**Predicted Exam Score: {result['predicted_exam_score']:.2f}**")
                else:
                    st.error(f"Prediction failed. Backend returned status code: {response.status_code}")
                    st.error(response.text)
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")

def view_history():
    st.subheader("Your Prediction History")
    try:
        response = requests.get(f"{BACKEND_URL}/history/filter", params={"name": st.session_state.student_name})
        if response.status_code == 200:
            data = response.json()
            if "data" in data and data["data"]:
                df = pd.DataFrame(data["data"])
                st.dataframe(df)
            else:
                st.info("No prediction history found.")
        else:
            st.error("Failed to fetch history")
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")

def view_progress():
    st.subheader("Your Progress Over Time")
    try:
        response = requests.get(f"{BACKEND_URL}/progress", params={"name": st.session_state.student_name})
        if response.status_code == 200:
            data = response.json()
            if "progress" in data and data["progress"]:
                df = pd.DataFrame(data["progress"])
                df["date"] = pd.to_datetime(df["date"])
                fig = px.line(df, x='date', y='Exam_Score', title='Exam Score Predictions Over Time', markers=True)
                st.plotly_chart(fig)
            else:
                st.info("No progress data found. Make a prediction first.")
        else:
            st.error("Failed to fetch progress")
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")

def main():
    st.title("AI Exam Score Predictor ")

    if not st.session_state.student_logged_in:
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        st.sidebar.title(f"Welcome, {st.session_state.student_name}")
        if st.sidebar.button("Logout"):
            st.session_state.student_logged_in = False
            st.session_state.student_name = None
            st.rerun()

        menu = ["Predict Score", "View History", "Progress Dashboard"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Predict Score":
            predict_score()
        elif choice == "View History":
            view_history()
        elif choice == "Progress Dashboard":
            view_progress()

if __name__ == "__main__":
    main()

