import os
import streamlit as st


def _get_setting(key):
    try:
        return st.secrets[key]
    except Exception:
        return os.environ.get(key)


# Database Configuration
DB_HOST = _get_setting("DB_HOST")
DB_PORT = _get_setting("DB_PORT")
DB_NAME = _get_setting("DB_NAME")
DB_USER = _get_setting("DB_USER")
DB_PASSWORD = _get_setting("DB_PASSWORD")


# Groq API Configuration
GROQ_API_KEY = _get_setting("GROQ_API_KEY")


# Application Configuration
APP_NAME = "Smart Loan Approval Prediction System"