
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Literal
import joblib
import pandas as pd
import sqlite3
from datetime import datetime
import hashlib
import os

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

DB_NAME = "ogperformance.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            Hours_Studied INTEGER,
            Attendance INTEGER,
            Parental_Involvement TEXT,
            Access_to_Resources TEXT,
            Sleep_Hours INTEGER,
            Previous_Scores INTEGER,
            Motivation_Level TEXT,
            Internet_Access TEXT,
            Tutoring_Sessions INTEGER,
            Family_Income TEXT,
            Teacher_Quality TEXT,
            Peer_Influence TEXT,
            Parental_Education_Level TEXT,
            predicted_score INTEGER,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

def create_students_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()

# Create FastAPI app
app = FastAPI(title = "AI Exam Score Predictor API")
# sqlite database setup
create_table()
# students tabel setup
create_students_table()

# Function to save prediction to database
def save_prediction(data, predicted_score):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO performance (
            name,
            Hours_Studied,
            Attendance,
            Parental_Involvement,
            Access_to_Resources,
            Sleep_Hours,
            Previous_Scores,
            Motivation_Level,
            Internet_Access,
            Tutoring_Sessions,
            Family_Income,
            Teacher_Quality,
            Peer_Influence,
            Parental_Education_Level,
            predicted_score,
            created_at
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data.name,
        data.Hours_Studied,
        data.Attendance,
        data.Parental_Involvement,
        data.Access_to_Resources,
        data.Sleep_Hours,
        data.Previous_Scores,
        data.Motivation_Level,
        data.Internet_Access,
        data.Tutoring_Sessions,
        data.Family_Income,
        data.Teacher_Quality,
        data.Peer_Influence,
        data.Parental_Education_Level,
        predicted_score,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

# Endpoint to get prediction history
def get_history(limit: int = 50):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            Hours_Studied,
            Attendance,
            Parental_Involvement,
            Access_to_Resources,
            Sleep_Hours,
            Previous_Scores,
            Motivation_Level,
            Internet_Access,
            Tutoring_Sessions,
            Family_Income,
            Teacher_Quality,
            Peer_Influence,
            Parental_Education_Level,
            predicted_score,
            created_at
        FROM performance
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append({
            "id" : row[0],
            "name" : row[1],
            "Hours_Studied" : row[2],
            "Attendance" : row[3],
            "Parental_Involvement" : row[4],
            "Access_to_Resources" : row[5],
            "Sleep_Hours" : row[6],
            "Previous_Scores" : row[7],
            "Motivation_Level" : row[8],
            "Internet_Access" : row[9],
            "Tutoring_Sessions" : row[10],
            "Family_Income" : row[11],
            "Teacher_Quality" : row[12],
            "Peer_Influence" : row[13],
            "Parental_Education_Level" : row[14],
            "predicted_score" : row[15],
            "created_at" : row[16],
        })

    return history 

# Endpoint to get prediction history filtered by name
def get_history_filtered(name: str = None, limit: int = 50):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if name:
        cursor.execute("""
            SELECT
                id,
                name,
                Hours_Studied,
                Attendance,
                Parental_Involvement,
                Access_to_Resources,
                Sleep_Hours,
                Previous_Scores,
                Motivation_Level,
                Internet_Access,
                Tutoring_Sessions,
                Family_Income,
                Teacher_Quality,
                Peer_Influence,
                Parental_Education_Level,
                predicted_score,
                created_at
            FROM performance
            WHERE name = ?
            ORDER BY id DESC
            LIMIT ?
        """, (name, limit))
    else:
        cursor.execute("""
            SELECT
                id,
                name,
                Hours_Studied,
                Attendance,
                Parental_Involvement,
                Access_to_Resources,
                Sleep_Hours,
                Previous_Scores,
                Motivation_Level,
                Internet_Access,
                Tutoring_Sessions,
                Family_Income,
                Teacher_Quality,
                Peer_Influence,
                Parental_Education_Level,
                predicted_score,
                created_at
            FROM performance
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    history = []
    for row in rows:
        history.append({
            "id" : row[0],
            "name" : row[1],
            "Hours_Studied" : row[2],
            "Attendance" : row[3],
            "Parental_Involvement" : row[4],
            "Access_to_Resources" : row[5],
            "Sleep_Hours" : row[6],
            "Previous_Scores" : row[7],
            "Motivation_Level" : row[8],
            "Internet_Access" : row[9],
            "Tutoring_Sessions" : row[10],
            "Family_Income" : row[11],
            "Teacher_Quality" : row[12],
            "Peer_Influence" : row[13],
            "Parental_Education_Level" : row[14],
            "predicted_score" : row[15],
            "created_at" : row[16],
        })

    return history

# Endpoint to get user progress over time
def get_user_progress(name: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            created_at,
            predicted_score
        FROM performance
        WHERE name = ?
        ORDER BY created_at ASC
    """, (name,))

    rows = cursor.fetchall()
    conn.close()

    progress = []
    for row in rows:
        progress.append({
            "date" : row[0],
            "Exam_Score" : row[1]
        })

    return progress

# Endpoint to get skill distribution for visualization
def get_score_distribution():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT predicted_score, COUNT(*)
        FROM performance
        GROUP BY predicted_score
    """)

    rows = cursor.fetchall()
    conn.close()
    
    distribution = {}
    for Exam_Score, count in rows:
        distribution[Exam_Score] = count

    return distribution

# Load ML pipeline
model = joblib.load("decision_tree_model.pkl")
ordinal_encoder = joblib.load("ordinal_encoder.pkl")

# Student authentication schema
class StudentAuth(BaseModel):
    username: str = Field(..., min_length = 3)
    password: str = Field(..., min_length = 4)

# Input schema
class ScoreInput(BaseModel):
    name: str = Field(..., min_length=1)
    Hours_Studied: int = Field(..., ge=0, le=24)
    Attendance: int = Field(..., ge=0,le=100)
    Parental_Involvement: Literal["Low","Medium","High"]
    Access_to_Resources: Literal["Low","Medium","High"]
    Sleep_Hours: int = Field(...,ge=0,le=24)
    Previous_Scores: int = Field(...,ge=0,le=100)
    Motivation_Level: Literal["Low","Medium","High"]
    Internet_Access: Literal["Yes","No"]
    Tutoring_Sessions: int = Field(..., ge=0, le=100)
    Family_Income: Literal["Low","Medium","High"]
    Teacher_Quality: Literal["Low","Medium","High"]
    Peer_Influence: Literal["Positive","Negative","Neutral"]
    Parental_Education_Level: Literal["High School", "College", "Postgraduate"]

@app.get("/")
def home():
    return {"message" : "AI Exam_Score Prediction API is running"}

@app.post("/predict")
def predict_exam_score(data: ScoreInput):
    try:
        # convert input into DataFrame
        input_df = pd.DataFrame([{
            "Hours_Studied": data.Hours_Studied,
            "Attendance" : data.Attendance,
            "Parental_Involvement" : data.Parental_Involvement,
            "Access_to_Resources" : data.Access_to_Resources,
            "Sleep_Hours" : data.Sleep_Hours,
            "Previous_Scores" : data.Previous_Scores,
            "Motivation_Level" : data.Motivation_Level,
            "Internet_Access" : data.Internet_Access,
            "Tutoring_Sessions" : data.Tutoring_Sessions,
            "Family_Income" : data.Family_Income,
            "Teacher_Quality" : data.Teacher_Quality,
            "Peer_Influence" : data.Peer_Influence,
            "Parental_Education_Level" : data.Parental_Education_Level,
        }])

        # Encode categorical features using ordinal_encoder
        cols_to_encode = ["Parental_Involvement","Access_to_Resources","Motivation_Level","Family_Income","Teacher_Quality","Parental_Education_Level","Peer_Influence"]
        input_df[cols_to_encode] = ordinal_encoder.transform(input_df[cols_to_encode])

        # Manually encode Internet_Access  which were LabelEncoded in the notebook
        input_df["Internet_Access"] = input_df["Internet_Access"].map({"No": 0, "Yes": 1})

        # Predict
        prediction = model.predict(input_df)
        predicted_score = float(prediction[0])
        # save to database
        save_prediction(data, predicted_score)

        return {
            "name" : data.name,
            "predicted_exam_score" : predicted_score
        }
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)} \nTraceback: {traceback.format_exc()}"
        )

@app.get("/history")
def fetch_history(limit: int = 50):
    return{
        "count" : limit,
        "data" : get_history(limit)
    }

@app.get("/analytics/score")
def exam_score_analytics():
    return get_score_distribution()

@app.get("/history/filter")
def fetch_history_filtered(name: str = None, limit: int = 50):
    return {
        "name": name,
        "count": limit,
        "data": get_history_filtered(name, limit)
    }

@app.get("/progress")
def user_progress(name: str):
    return {
        "name": name,
        "progress": get_user_progress(name)
    }

# Endpoint for student registration
@app.post("/student/register")
def register_student(data: StudentAuth):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO students (username, password_hash, created_at)
            VALUES (?, ?, ?)
        """, (
            data.username,
            hash_password(data.password),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        return {"message" : "Student registered successfully"}
    
    except sqlite3.IntegrityError:
        return {"error": "Username already exists"}
    
    finally:
        conn.close()

# Endpoint for student login
@app.post("/student/login")
def login_student(data: StudentAuth):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT password_hash FROM students WHERE username = ?
    """, (data.username,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error" : "User not Found"}
    
    if row[0] != hash_password(data.password):
        return {"error ": "Invalid_password"}
    
    return {"message": "Login succcessful", "username" : data.username}