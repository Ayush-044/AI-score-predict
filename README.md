# AI Score Predictor

## Overview

The **AI Score Predictor** is a machine learning–based web application that predicts a student's **exam score** based on multiple academic and behavioral factors.

The system uses a trained machine learning model to estimate the expected score by analyzing inputs such as study hours, attendance, parental involvement, access to resources, and other learning factors.

This project demonstrates how **Machine Learning, FastAPI backend services, and data analysis tools** can be combined to build an intelligent prediction system.

---

# Features

## Student

* Predict exam score using AI
* Input multiple academic factors
* Instant prediction results
* Simple and interactive interface

## System

* Machine learning based score prediction
* REST API built with FastAPI
* Data processing with Pandas
* Model inference using Scikit-learn
* SQLite database

---

# Tech Stack

**Frontend**

* Streamlit

**Backend**

* FastAPI

**Database**

* SQLite

**Machine Learning**

* Scikit-learn

**Data Analysis**

* Pandas

**Model Serialization**

* Joblib

---

# Project Structure

```
AI-score-predict/
│
├── bperformance.py
├── fperformance.py
├── decision_tree_model.pkl
├── ordinal_encoder.pkl
├── student_performance.ipynb
├── StudentPerformanceFactors.csv
├── requirements.txt
├── .gitignore
```

---

# How to Clone the Repository

```bash
git clone https://github.com/Ayush-044/AI-score-predict.git
```

---

# How to Run Locally

## Note

Python **3.11** is recommended to install the dependencies correctly.

To view the database file, you can install **DB Browser for SQLite**.

---

# Create Virtual Environment

```bash
python3.11 -m venv .vnv
```

---

# Activate Virtual Environment

### On Windows

```bash
.venv\Scripts\activate
```

### On macOS / Linux

```bash
source .venv/bin/activate
```

---

# 1 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 2 Start Backend Server

```bash
python -m uvicorn bperformance:app --reload
```

---

# 3 Start Frontend Application

```bash
streamlit run fperformance.py
```

---

# Deactivate Virtual Environment

```bash
deactivate
```

OR

Press

```
CTRL + C
```

---

# Project Goal

The goal of this project is to demonstrate how **Machine Learning models can be integrated with a full-stack application** to predict student performance.

This project highlights skills in:

* Machine Learning Model Development
* FastAPI Backend Development
* Data Processing with Pandas
* API Integration
* Full Stack AI Application Development

---
