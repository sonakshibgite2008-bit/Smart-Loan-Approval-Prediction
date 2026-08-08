from database import engine
from sqlalchemy import text


with engine.begin() as connection:

    connection.execute(
        text("""
            CREATE TABLE IF NOT EXISTS user_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                uploaded_at TIMESTAMP NOT NULL
            )
        """)
    )


print("✅ user_documents table created successfully!")