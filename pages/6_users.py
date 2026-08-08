import streamlit as st
import pandas as pd
from database import engine
from sqlalchemy import text

st.set_page_config(
    page_title="Registered Users",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Registered Users")
st.caption("View all users who have registered in the system.")

try:

    with engine.connect() as conn:
        users = conn.execute(
            text("""
                SELECT
                    id,
                    full_name,
                    email,
                    phone
                FROM users
                ORDER BY id DESC
            """)
        ).mappings().all()

    total_users = len(users)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="👥 Total Registered Users",
            value=total_users
        )

    with col2:
        st.metric(
            label="📊 User Records",
            value=total_users
        )

    st.divider()

    if users:

        df = pd.DataFrame(users)

        search = st.text_input(
            "🔍 Search User",
            placeholder="Search by name, email or phone..."
        )

        if search:

            search = search.lower()

            df = df[
                df["full_name"].astype(str).str.lower().str.contains(search)
                |
                df["email"].astype(str).str.lower().str.contains(search)
                |
                df["phone"].astype(str).str.lower().str.contains(search)
            ]

        st.subheader("📋 Registered Users List")

        if len(df) > 0:

            df = df.rename(
                columns={
                    "id": "User ID",
                    "full_name": "Full Name",
                    "email": "Email",
                    "phone": "Phone"
                }
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.success(
                f"Showing {len(df)} registered user(s)."
            )

        else:

            st.warning(
                "No users found matching your search."
            )

    else:

        st.info(
            "No users registered yet."
        )

except Exception as e:

    st.error(
        f"Unable to load registered users: {e}"
    )
