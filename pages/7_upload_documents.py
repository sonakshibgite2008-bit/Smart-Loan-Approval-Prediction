import streamlit as st
import os
from datetime import datetime

st.set_page_config(
    page_title="Upload Documents",
    page_icon="📄",
    layout="wide"
)

# ----------------------------
# Login Check
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("Please login first.")
    st.stop()

# ----------------------------
# Upload Folder
# ----------------------------
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----------------------------
# Title
# ----------------------------
st.title("📄 Upload Loan Documents")

st.write("Upload the required documents for loan approval prediction.")

st.divider()

# ----------------------------
# File Upload
# ----------------------------
uploaded_files = st.file_uploader(
    "Choose Documents",
    type=["pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:

    for file in uploaded_files:

        filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + file.name

        save_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        with open(save_path, "wb") as f:
            f.write(file.getbuffer())

        st.success(f"✅ {file.name} uploaded successfully!")

st.divider()

st.subheader("Required Documents")

st.markdown("""
- 📄 Salary Slip
- 🏦 Bank Statement
- 🪪 Aadhaar Card
- 💳 PAN Card
- 📜 Income Certificate
""")

st.info("Supported formats: PDF, JPG, JPEG, PNG")
