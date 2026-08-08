import streamlit as st
from auth import register_user

st.set_page_config(
    page_title="Register",
    page_icon="📝",
    layout="centered"
)

st.title("📝 Create Account")
st.write("Register to use the Smart Loan Approval Prediction System")

with st.form("register_form"):

    full_name = st.text_input("Full Name")

    email = st.text_input("Email")

    phone = st.text_input("Phone Number")

    password = st.text_input("Password", type="password")

    confirm_password = st.text_input("Confirm Password", type="password")

    submit = st.form_submit_button("Register")

if submit:

    if full_name == "":
        st.error("Enter Full Name")

    elif email == "":
        st.error("Enter Email")

    elif phone == "":
        st.error("Enter Phone Number")

    elif password == "":
        st.error("Enter Password")

    elif password != confirm_password:
        st.error("Passwords do not match")

    else:

        success, message = register_user(
            full_name,
            email,
            phone,
            password
        )

        if success:
            st.success(message)
            st.balloons()

        else:
            st.error(message)
st.write("Password bytes:", len(password.encode("utf-8")))