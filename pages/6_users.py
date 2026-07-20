import streamlit as st
from database import engine
from sqlalchemy import text


st.set_page_config(
    page_title="Registered Users",
    page_icon="👥",
    layout="wide"
)


st.title("👥 Registered Users")


try:

    with engine.connect() as conn:

        users = conn.execute(
            text("""
                SELECT 
                    id,
                    full_name,
                    email,
                    phone,
                    created_at
                FROM users
                ORDER BY id DESC
            """)
        ).mappings().all()


    if users:

        st.success(f"Total Registered Users: {len(users)}")


        for user in users:

            with st.container():

                st.markdown(
                    f"""
                    ### 👤 {user['full_name']}

                    📧 Email: {user['email']}  
                    📱 Phone: {user['phone']}  
                    🕒 Registered: {user['created_at']}
                    """
                )

                st.divider()

    else:

        st.info("No users registered yet.")


except Exception as e:

    st.error(e)