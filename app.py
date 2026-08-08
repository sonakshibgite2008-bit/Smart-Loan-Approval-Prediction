import streamlit as st
from prediction import predict_loan

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Smart Loan Approval Prediction",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Logout Button

if st.session_state.get("logged_in"):

    with st.sidebar:

        st.write(
            f"👋 Welcome {st.session_state.user_name}"
        )


        if st.button("🚪 Logout"):

            st.session_state.logged_in = False
            st.session_state.user_name = ""
            st.session_state.user_id = None

            st.switch_page(
                "pages/2_login.py"
            )

# -----------------------------
# Session State
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main{
    background-color:#F5F7FA;
}

.title{
    text-align:center;
    color:#003366;
    font-size:45px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:gray;
    font-size:20px;
}

.feature-card{
    background:white;
    padding:25px;
    border-radius:15px;
    box-shadow:0px 3px 10px rgba(0,0,0,0.15);
    text-align:center;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:40px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    "<h1 class='title'>🏦 Smart Loan Approval Prediction System</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Machine Learning Based Loan Approval Prediction</p>",
    unsafe_allow_html=True
)

st.divider()

# -----------------------------
# Welcome Section
# -----------------------------
left, right = st.columns([2,1])

with left:

    st.subheader("Welcome 👋")

    st.write("""
This project predicts whether a loan application is likely to be approved
using Machine Learning.

### Features

- 🔐 Secure Login & Register
- 📄 Upload Loan Documents
- 📊 Dataset Analysis
- 🤖 Loan Prediction
- 📜 Prediction History
- 📈 Interactive Dashboard
- 💾 PostgreSQL Database
    """)

with right:

    st.info("""
Project Modules

🏠 Home

🔐 Login

📝 Register

📊 Dashboard

📄 Upload Documents

📈 Analysis

🤖 Prediction

📜 History

👤 Profile
""")

st.divider()

# -----------------------------
# Feature Cards
# -----------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("## 📄 Upload Documents")
    st.write("""
    Upload Salary Slip  
    Upload Bank Statement  
    Upload Income Certificate
    """)

    if st.button("Go to Upload Documents"):
        st.switch_page("pages/7_upload_documents.py")


with col2:
    st.markdown("## 🤖 AI Prediction")
    st.write("""
    Predict Loan Status  
    Confidence Score  
    Risk Analysis
    """)

    if st.button("Start Prediction"):
        st.switch_page("pages/10_predict.py")


with col3:
    st.markdown("## 📈 Dashboard")
    st.write("""
    Visual Analytics  
    Loan Reports  
    Prediction History
    """)

    if st.button("View Dashboard"):
        st.switch_page("pages/5_dashboard.py")

st.divider()

st.markdown(
"<div class='footer'>© 2026 Smart Loan Approval Prediction System</div>",
unsafe_allow_html=True
)
# -----------------------------
# Loan Prediction Section
# -----------------------------

st.divider()

st.header("🤖 Loan Approval Prediction")


st.write(
    "Enter applicant details below to check loan approval probability."
)


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

    dependents = st.selectbox(
        "Dependents",
        ["0", "1", "2", "3+"]
    )

    education = st.selectbox(
        "Education",
        ["Graduate", "Not Graduate"]
    )

    self_employed = st.selectbox(
        "Self Employed",
        ["Yes", "No"]
    )


with col2:

    applicant_income = st.number_input(
        "Applicant Income",
        min_value=0
    )

    coapplicant_income = st.number_input(
        "Coapplicant Income",
        min_value=0
    )

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0
    )

    loan_term = st.number_input(
        "Loan Term (months)",
        value=360
    )

    credit_history = st.selectbox(
        "Credit History",
        [1.0, 0.0]
    )

    property_area = st.selectbox(
        "Property Area",
        ["Urban", "Rural", "Semiurban"]
    )


if st.button("🔍 Predict Loan Status"):


    input_data = {

        "Loan_ID": 0,

        "Gender": gender,

        "Married": married,

        "Dependents": dependents,

        "Education": education,

        "Self_Employed": self_employed,

        "ApplicantIncome": applicant_income,

        "CoapplicantIncome": coapplicant_income,

        "LoanAmount": loan_amount,

        "Loan_Amount_Term": loan_term,

        "Credit_History": credit_history,

        "Property_Area": property_area
    }


    result = predict_loan(input_data)


    if result == "Approved":

        st.success(
            "🎉 Congratulations! Loan is Approved"
        )

    else:

        st.error(
            "❌ Sorry! Loan is Not Approved"
        )