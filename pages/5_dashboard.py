import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import text
from database import engine


st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)


st.title("📊 Smart Loan Approval Dashboard")

st.markdown("""
<style>

.metric-card{
background:white;
padding:20px;
border-radius:15px;
box-shadow:0px 3px 10px rgba(0,0,0,0.15);
text-align:center;
}

</style>
""", unsafe_allow_html=True)



if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()



try:

    with engine.connect() as conn:

        users = pd.read_sql(
            text("SELECT * FROM users"),
            conn
        )


        history = pd.read_sql(
            text("""
            SELECT *
            FROM prediction_history
            ORDER BY created_at DESC
            """),
            conn
        )


    total_users = len(users)
    total_predictions = len(history)


    approved = len(
        history[
            history["result"]=="Approved"
        ]
    )


    rejected = len(
        history[
            history["result"]=="Rejected"
        ]
    )


    rate = 0

    if total_predictions:
        rate = round(
            approved/total_predictions*100,
            2
        )



    # Metrics

    c1,c2,c3,c4,c5 = st.columns(5)


    c1.metric(
        "👥 Total Users",
        total_users
    )


    c2.metric(
        "📄 Predictions",
        total_predictions
    )


    c3.metric(
        "✅ Approved",
        approved
    )


    c4.metric(
        "❌ Rejected",
        rejected
    )


    c5.metric(
        "📈 Approval %",
        f"{rate}%"
    )



    st.divider()



    # Charts

    if total_predictions > 0:


        col1,col2 = st.columns(2)


        with col1:

            st.subheader(
                "Loan Status Distribution"
            )


            pie_data = history["result"].value_counts().reset_index()

            pie_data.columns=[
                "Status",
                "Count"
            ]


            fig = px.pie(
                pie_data,
                names="Status",
                values="Count",
                hole=0.4
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )



        with col2:

            st.subheader(
                "Prediction Overview"
            )


            fig2 = px.bar(
                pie_data,
                x="Status",
                y="Count",
                text="Count"
            )


            st.plotly_chart(
                fig2,
                use_container_width=True
            )



        st.divider()



        st.subheader(
            "📜 Recent Prediction History"
        )


        st.dataframe(
            history.head(10),
            use_container_width=True
        )


    else:

        st.info(
            "No predictions available yet."
        )



except Exception as e:

    st.error(e)