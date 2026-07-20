from sqlalchemy import text
from database import engine
import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(
    page_title="Loan Prediction",
    page_icon="🏦",
    layout="wide"
)

# -----------------------------
# Login Check
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

st.title("🏦 Loan Approval Prediction")

st.markdown("---")

# -----------------------------
# Load Model
# -----------------------------
MODEL_PATH = "models/loan_model.pkl"

model = None

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    st.warning("Model not found. Please train the model first.")

# -----------------------------
# Input Form
# -----------------------------
col1, col2 = st.columns(2)

with col1:

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    married = st.selectbox(
        "Married",
        ["Yes", "No"]
    )

    education = st.selectbox(
        "Education",
        ["Graduate", "Not Graduate"]
    )

    self_employed = st.selectbox(
        "Self Employed",
        ["Yes", "No"]
    )

    applicant_income = st.number_input(
        "Applicant Income",
        min_value=0
    )

with col2:

    co_income = st.number_input(
        "Co Applicant Income",
        min_value=0
    )

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0
    )

    loan_term = st.number_input(
        "Loan Amount Term",
        value=360
    )

    credit_history = st.selectbox(
        "Credit History",
        [1, 0]
    )

    property_area = st.selectbox(
        "Property Area",
        ["Urban", "Semiurban", "Rural"]
    )

st.markdown("---")

if st.button("Predict Loan"):

    if model is None:
        st.error("Train the model first.")

    else:

        gender_value = 1 if gender == "Male" else 0
        married_value = 1 if married == "Yes" else 0
        education_value = 0 if education == "Graduate" else 1
        self_employed_value = 1 if self_employed == "Yes" else 0

        if property_area == "Urban":
            property_value = 2
        elif property_area == "Semiurban":
            property_value = 1
        else:
            property_value = 0


        data = pd.DataFrame([[
            0,
            gender_value,
            married_value,
            0,
            education_value,
            self_employed_value,
            applicant_income,
            co_income,
            loan_amount,
            loan_term,
            credit_history,
            property_value
        ]],
        columns=[
            "Loan_ID",
            "Gender",
            "Married",
            "Dependents",
            "Education",
            "Self_Employed",
            "ApplicantIncome",
            "CoapplicantIncome",
            "LoanAmount",
            "Loan_Amount_Term",
            "Credit_History",
            "Property_Area"
        ])


        prediction = model.predict(data)[0]
        
        if prediction == 1:
            result = "Approved"
            st.success("✅ Loan Approved")
        else:
            result = "Rejected"
            st.error("❌ Loan Rejected")

try:

    with engine.begin() as conn:

        conn.execute(
            text("""
            INSERT INTO prediction_history
            (
                user_id,
                gender,
                married,
                education,
                income,
                loan_amount,
                property_area,
                result
            )
            VALUES
            (
                :user_id,
                :gender,
                :married,
                :education,
                :income,
                :loan_amount,
                :property_area,
                :result
            )
            """),
            {
                "user_id": st.session_state.get("user_id", 1),
                "gender": gender,
                "married": married,
                "education": education,
                "income": applicant_income,
                "loan_amount": loan_amount,
                "property_area": property_area,
                "result": result
            }
        )

    st.info("Prediction saved ✅")

except Exception as e:
    st.error(e)

st.write("DEBUG RESULT:", result)