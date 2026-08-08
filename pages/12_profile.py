import streamlit as st
from sqlalchemy import text
from database import engine


st.set_page_config(
    page_title="Profile",
    page_icon="👤",
    layout="centered"
)


st.title("👤 User Profile")


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()


user_id = st.session_state.get("user_id", 1)


try:

    with engine.connect() as conn:

        user = conn.execute(
            text("""
            SELECT *
            FROM users
            WHERE id = :id
            """),
            {
                "id": user_id
            }
        ).mappings().fetchone()


    if user:

        st.success("Profile Loaded ✅")


        st.subheader("Personal Information")

        st.write(
            "👤 Name:",
            user["full_name"]
        )

        st.write(
            "📧 Email:",
            user["email"]
        )

        st.write(
            "📱 Phone:",
            user["phone"]
        )


        st.divider()

        st.subheader("Update Profile")


        new_name = st.text_input(
            "Full Name",
            user["full_name"]
        )

        new_phone = st.text_input(
            "Phone",
            user["phone"]
        )


        if st.button("Update Profile"):

            with engine.begin() as conn:

                conn.execute(
                    text("""
                    UPDATE users
                    SET
                    full_name=:name,
                    phone=:phone
                    WHERE id=:id
                    """),
                    {
                        "name":new_name,
                        "phone":new_phone,
                        "id":user_id
                    }
                )

            st.success("Profile Updated Successfully ✅")


    else:

        st.error("User not found")


except Exception as e:

    st.error(e)