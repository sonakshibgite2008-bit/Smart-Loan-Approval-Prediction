import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Dataset",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Loan Dataset Analysis")

DATA_PATH = "dataset/load_dataset.csv"

if os.path.exists(DATA_PATH):

    df = pd.read_csv(DATA_PATH)

    st.success("Dataset Loaded Successfully ✅")

    # Total Records
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Records",
            len(df)
        )

    with col2:
        st.metric(
            "Total Columns",
            len(df.columns)
        )

    with col3:
        missing = df.isnull().sum().sum()
        st.metric(
            "Missing Values",
            missing
        )


    st.divider()

    # Dataset Preview
    st.subheader("🔍 Dataset Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )


    st.divider()

    # Columns
    st.subheader("📌 Dataset Columns")

    st.write(list(df.columns))


    st.divider()

    # Missing Values
    st.subheader("⚠️ Missing Values")

    missing_df = pd.DataFrame(
        {
            "Column": df.columns,
            "Missing Count": df.isnull().sum()
        }
    )

    st.dataframe(
        missing_df,
        use_container_width=True
    )

else:

    st.error("Dataset file not found!")