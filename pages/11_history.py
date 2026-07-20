import streamlit as st
import pandas as pd
from sqlalchemy import text
from database import engine


st.set_page_config(
    page_title="History",
    page_icon="📜",
    layout="wide"
)


st.title("📜 Loan Prediction History")


try:

    with engine.connect() as conn:

        df = pd.read_sql(
            text("""
            SELECT *
            FROM prediction_history
            ORDER BY created_at DESC
            """),
            conn
        )


    if len(df) > 0:

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.info("No prediction history found.")


except Exception as e:

    st.error(e)