import streamlit as st


st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)


st.title("ℹ️ About Smart Loan Approval Prediction System")


st.markdown("""
## 🏦 Smart Loan Approval Prediction System

This project is a Machine Learning based application that predicts
whether a loan application will be approved or rejected.

The system uses applicant details and a trained Machine Learning model
to provide prediction results.

---

## 🤖 Technologies Used

### Frontend
- Streamlit
- Python
- HTML/CSS Styling

### Backend
- Python
- PostgreSQL Database
- SQLAlchemy

### Machine Learning
- Pandas
- Scikit-Learn
- Random Forest Classifier

---

## ✨ Features

✅ User Registration & Login

✅ Secure Password Encryption

✅ Loan Approval Prediction

✅ Prediction History

✅ Dataset Analysis

✅ Data Visualization Dashboard

✅ User Profile Management

---

## 📊 Machine Learning Model

Algorithm Used:

**Random Forest Classifier**

Model Performance:

Accuracy ≈ 82%

---

## 👩‍💻 Project Developed By

**Sonakshi Gite**

Artificial Intelligence & Machine Learning Student

---

## 🎯 Project Objective

The main objective of this project is to help users estimate
loan approval probability using Machine Learning techniques.
""")