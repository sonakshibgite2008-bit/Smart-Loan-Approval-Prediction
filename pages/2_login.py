import streamlit as st
from auth import login_user


st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)


st.markdown("""
<style>

.login-card{
    background:white;
    padding:30px;
    border-radius:20px;
    box-shadow:0px 5px 20px rgba(0,0,0,0.15);
}

h1{
    text-align:center;
}

</style>
""", unsafe_allow_html=True)



st.markdown(
    "<h1>🔐 Login</h1>",
    unsafe_allow_html=True
)


st.write(
    "Login to access Smart Loan Approval Prediction System"
)


with st.container():

    email = st.text_input(
        "📧 Email"
    )

    password = st.text_input(
        "🔑 Password",
        type="password"
    )


    if st.button(
        "Login",
        use_container_width=True
    ):


        if email == "" or password == "":
            st.error(
                "Please enter email and password"
            )


        else:

            success, result = login_user(
                email,
                password
            )
            st.write("DEBUG:", success, result)


            if success:

                st.session_state.logged_in = True
                st.session_state.user_id = result["id"]
                st.session_state.user_name = result["full_name"]


                st.success(
                    "Login Successful 🎉"
                )


                st.switch_page(
    "pages/5_dashboard.py"
)


            else:

                st.error(result)