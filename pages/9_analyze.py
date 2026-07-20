import streamlit as st
import pandas as pd
import plotly.express as px
import os


st.set_page_config(
    page_title="Data Analysis",
    page_icon="📈",
    layout="wide"
)


st.title("📈 Loan Dataset Analysis Dashboard")


DATA_PATH = "dataset/load_dataset.csv"


if os.path.exists(DATA_PATH):

    df = pd.read_csv(DATA_PATH)

    st.success("Dataset Loaded Successfully ✅")


    # -----------------------------
    # Overview
    # -----------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Applications",
            len(df)
        )

    with col2:
        approved = len(
            df[df["Loan_Status"]=="Y"]
        )
        st.metric(
            "Approved Loans",
            approved
        )

    with col3:
        rejected = len(
            df[df["Loan_Status"]=="N"]
        )
        st.metric(
            "Rejected Loans",
            rejected
        )


    st.divider()


    # -----------------------------
    # Loan Status Chart
    # -----------------------------

    st.subheader("🏦 Loan Approval Distribution")

    status_chart = px.pie(
        df,
        names="Loan_Status",
        title="Approved vs Rejected Loans"
    )

    st.plotly_chart(
        status_chart,
        use_container_width=True
    )


    # -----------------------------
    # Gender Analysis
    # -----------------------------

    st.subheader("👤 Gender Wise Analysis")

    gender_chart = px.bar(
        df["Gender"].value_counts(),
        title="Applications by Gender"
    )

    st.plotly_chart(
        gender_chart,
        use_container_width=True
    )


    # -----------------------------
    # Education Analysis
    # -----------------------------

    st.subheader("🎓 Education Analysis")

    edu_chart = px.bar(
        df["Education"].value_counts(),
        title="Graduate vs Non Graduate"
    )

    st.plotly_chart(
        edu_chart,
        use_container_width=True
    )


    # -----------------------------
    # Property Area
    # -----------------------------

    st.subheader("🏠 Property Area Analysis")

    property_chart = px.bar(
        df["Property_Area"].value_counts(),
        title="Applications by Property Area"
    )

    st.plotly_chart(
        property_chart,
        use_container_width=True
    )


else:

    st.error("Dataset not found!")