import os
from datetime import datetime
from pathlib import Path

import streamlit as st
from sqlalchemy import text

from database import engine


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Upload Documents",
    page_icon="📄",
    layout="wide"
)


# =========================================================
# CREATE USER_DOCUMENTS TABLE
# =========================================================
# This will automatically create the table if it does not exist.
# =========================================================

with engine.begin() as connection:

    connection.execute(
        text("""
            CREATE TABLE IF NOT EXISTS user_documents (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                uploaded_at TIMESTAMP NOT NULL
            )
        """)
    )


# =========================================================
# LOGIN CHECK
# =========================================================

if not st.session_state.get("logged_in", False):

    st.error(
        "You are not authorized to access this page."
    )

    st.info(
        "Please login first to access the Documents page."
    )

    st.stop()


# =========================================================
# GET LOGGED-IN USER DETAILS
# =========================================================

user_id = st.session_state.get(
    "user_id"
)

user_name = st.session_state.get(
    "user_name",
    "User"
)

user_email = st.session_state.get(
    "user_email",
    ""
)


# =========================================================
# USER ID CHECK
# =========================================================

if user_id is None:

    st.error(
        "User ID not found."
    )

    st.warning(
        "Please logout and login again."
    )

    st.stop()


# =========================================================
# UPLOAD SETTINGS
# =========================================================

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".jpg",
    ".jpeg",
    ".png"
}

MAX_FILE_SIZE_MB = 5

UPLOAD_ROOT = os.path.join(
    "uploads",
    "user_documents"
)


# =========================================================
# CREATE USER-SPECIFIC FOLDER
# =========================================================

user_folder = os.path.join(
    UPLOAD_ROOT,
    str(user_id)
)

os.makedirs(
    user_folder,
    exist_ok=True
)


# =========================================================
# PAGE HEADER
# =========================================================

st.title(
    "📄 Upload Documents"
)

st.write(
    f"Welcome, **{user_name}** 👋"
)

st.write(
    "Upload your documents for the loan application."
)


st.divider()


# =========================================================
# USER INFORMATION
# =========================================================

with st.expander(
    "👤 My Account Information"
):

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**User ID:** {user_id}"
        )

        st.write(
            f"**Name:** {user_name}"
        )

    with col2:

        st.write(
            f"**Email:** {user_email}"
        )


st.divider()


# =========================================================
# DOCUMENT UPLOAD SECTION
# =========================================================

st.subheader(
    "📤 Upload Your Document"
)

st.info(
    "Allowed formats: PDF, JPG, JPEG, PNG | Maximum size: 5 MB"
)


uploaded_file = st.file_uploader(
    "Choose a document",
    type=[
        "pdf",
        "jpg",
        "jpeg",
        "png"
    ],
    key="document_uploader"
)


# =========================================================
# UPLOAD BUTTON
# =========================================================

if st.button(
    "📤 Upload Document",
    use_container_width=True
):

    # =====================================================
    # CHECK FILE
    # =====================================================

    if uploaded_file is None:

        st.warning(
            "⚠️ Please select a document first."
        )

    else:

        # =================================================
        # GET FILE EXTENSION
        # =================================================

        file_extension = Path(
            uploaded_file.name
        ).suffix.lower()


        # =================================================
        # CHECK FILE EXTENSION
        # =================================================

        if file_extension not in ALLOWED_EXTENSIONS:

            st.error(
                "❌ Invalid file type."
            )

            st.info(
                "Only PDF, JPG, JPEG and PNG files are allowed."
            )


        else:

            # =============================================
            # CHECK FILE SIZE
            # =============================================

            file_size_mb = (
                uploaded_file.size
                / (1024 * 1024)
            )


            if file_size_mb > MAX_FILE_SIZE_MB:

                st.error(
                    f"❌ File size is {file_size_mb:.2f} MB."
                )

                st.warning(
                    "Maximum allowed file size is 5 MB."
                )


            else:

                try:

                    # =====================================
                    # CREATE UNIQUE FILE NAME
                    # =====================================

                    timestamp = datetime.now().strftime(
                        "%Y%m%d_%H%M%S_%f"
                    )

                    saved_file_name = (
                        f"{timestamp}_{uploaded_file.name}"
                    )


                    # =====================================
                    # CREATE FILE PATH
                    # =====================================

                    file_path = os.path.join(
                        user_folder,
                        saved_file_name
                    )


                    # =====================================
                    # SAVE FILE TO FOLDER
                    # =====================================

                    with open(
                        file_path,
                        "wb"
                    ) as file:

                        file.write(
                            uploaded_file.getbuffer()
                        )


                    # =====================================
                    # SAVE DOCUMENT RECORD IN DATABASE
                    # =====================================

                    with engine.begin() as connection:

                        connection.execute(
                            text("""
                                INSERT INTO user_documents
                                (
                                    user_id,
                                    file_name,
                                    file_path,
                                    uploaded_at
                                )
                                VALUES
                                (
                                    :user_id,
                                    :file_name,
                                    :file_path,
                                    :uploaded_at
                                )
                            """),
                            {
                                "user_id": user_id,
                                "file_name": uploaded_file.name,
                                "file_path": file_path,
                                "uploaded_at": datetime.now()
                            }
                        )


                    # =====================================
                    # SUCCESS
                    # =====================================

                    st.success(
                        "✅ Document uploaded successfully!"
                    )

                    st.info(
                        f"📄 {uploaded_file.name}"
                    )


                    # =====================================
                    # REFRESH PAGE
                    # =====================================

                    st.rerun()


                except Exception as e:

                    st.error(
                        "❌ Error while uploading document."
                    )

                    st.exception(e)


# =========================================================
# MY UPLOADED DOCUMENTS
# =========================================================

st.divider()

st.subheader(
    "📂 My Uploaded Documents"
)


try:

    # =====================================================
    # FETCH DOCUMENTS FOR CURRENT USER
    # =====================================================

    with engine.connect() as connection:

        documents = connection.execute(
            text("""
                SELECT
                    id,
                    file_name,
                    file_path,
                    uploaded_at
                FROM user_documents
                WHERE user_id = :user_id
                ORDER BY uploaded_at DESC
            """),
            {
                "user_id": user_id
            }
        ).fetchall()


    # =====================================================
    # SHOW DOCUMENTS
    # =====================================================

    if documents:

        st.success(
            f"✅ {len(documents)} document(s) uploaded."
        )


        for document in documents:

            # =============================================
            # DOCUMENT CONTAINER
            # =============================================

            col1, col2 = st.columns(
                [4, 1]
            )


            # =============================================
            # DOCUMENT INFORMATION
            # =============================================

            with col1:

                st.write(
                    f"📄 **{document.file_name}**"
                )

                st.caption(
                    f"Uploaded on: {document.uploaded_at}"
                )


            # =============================================
            # DOWNLOAD BUTTON
            # =============================================

            with col2:

                if os.path.exists(
                    document.file_path
                ):

                    try:

                        with open(
                            document.file_path,
                            "rb"
                        ) as file:

                            file_data = file.read()


                        st.download_button(
                            label="⬇️ Download",
                            data=file_data,
                            file_name=document.file_name,
                            key=f"download_{document.id}",
                            use_container_width=True
                        )


                    except Exception as e:

                        st.error(
                            "Unable to download file."
                        )

                        st.exception(e)


                else:

                    st.warning(
                        "File not found."
                    )


            st.divider()


    # =====================================================
    # NO DOCUMENTS
    # =====================================================

    else:

        st.info(
            "📂 No documents uploaded yet."
        )


# =========================================================
# DATABASE ERROR
# =========================================================

except Exception as e:

    st.error(
        "❌ Could not load uploaded documents."
    )

    st.exception(e)