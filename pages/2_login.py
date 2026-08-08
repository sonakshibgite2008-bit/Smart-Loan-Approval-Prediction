import streamlit as st
from auth import login_user


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)


# =========================
# CSS
# =========================

st.markdown("""
<style>

.login-card {
    background-color: white;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.15);
}

</style>
""", unsafe_allow_html=True)


# =========================
# INITIALIZE SESSION STATE
# =========================

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

if "user_name" not in st.session_state:
    st.session_state["user_name"] = None

if "user_email" not in st.session_state:
    st.session_state["user_email"] = None

if "role" not in st.session_state:
    st.session_state["role"] = None


# =========================
# ALREADY LOGGED IN
# =========================

if st.session_state["logged_in"]:

    st.success(
        f"Already logged in as {st.session_state['user_name']}"
    )

    st.write(
        f"📧 Email: {st.session_state['user_email']}"
    )

    st.write(
        f"👤 Role: {st.session_state['role']}"
    )

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state["logged_in"] = False
        st.session_state["user_id"] = None
        st.session_state["user_name"] = None
        st.session_state["user_email"] = None
        st.session_state["role"] = None

        st.success("Logged out successfully!")

        st.rerun()

    st.stop()


# =========================
# LOGIN PAGE
# =========================

st.markdown(
    "<h1 style='text-align:center;'>🔐 Login</h1>",
    unsafe_allow_html=True
)

st.write(
    "Login to access Smart Loan Approval Prediction System"
)


# =========================
# LOGIN FORM
# =========================

with st.container():

    email = st.text_input(
        "📧 Email",
        key="login_email"
    )

    password = st.text_input(
        "🔑 Password",
        type="password",
        key="login_password"
    )


    login_clicked = st.button(
        "Login",
        key="login_button",
        use_container_width=True
    )


# =========================
# LOGIN PROCESS
# =========================

if login_clicked:

    if email.strip() == "" or password.strip() == "":

        st.error(
            "Please enter email and password."
        )

    else:

        try:

            success, result = login_user(
                email.strip(),
                password
            )


            if success:

                # =========================
                # SAVE LOGIN SESSION
                # =========================

                st.session_state["logged_in"] = True

                st.session_state["user_id"] = result["id"]

                st.session_state["user_name"] = result["full_name"]

                st.session_state["user_email"] = result["email"]

                st.session_state["role"] = result["role"]


                st.success(
                    "✅ Login successful!"
                )

                st.write(
                    f"Welcome, {result['full_name']}!"
                )


                # =========================
                # REFRESH PAGE
                # =========================

                st.rerun()


            else:

                st.error(
                    result
                )


        except Exception as e:

            st.error(
                "Login failed."
            )

            st.exception(e)