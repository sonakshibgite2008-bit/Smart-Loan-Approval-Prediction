import os

from passlib.context import CryptContext
from sqlalchemy import text

from database import engine


# ===================================================
# PASSWORD HASHING
# ===================================================

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)


def hash_password(password):
    password = str(password)

    # Limit password length
    password = password.encode("utf-8")[:72].decode(
        "utf-8",
        errors="ignore"
    )

    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    plain_password = str(plain_password)

    plain_password = plain_password.encode("utf-8")[:72].decode(
        "utf-8",
        errors="ignore"
    )

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ===================================================
# ENSURE USERS TABLE
# ===================================================

def _ensure_users_schema():

    with engine.begin() as conn:

        # Create users table if it doesn't exist
        conn.execute(
            text("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    phone TEXT,
                    password TEXT NOT NULL,
                    role TEXT DEFAULT 'customer'
                )
            """)
        )

        # Check if role column exists
        try:

            conn.execute(
                text("""
                    ALTER TABLE users
                    ADD COLUMN role TEXT DEFAULT 'customer'
                """)
            )

        except Exception:
            # Column already exists
            pass


# Run schema check
_ensure_users_schema()


# ===================================================
# REGISTER USER
# ===================================================

def register_user(
    full_name,
    email,
    phone,
    password
):

    try:

        email = str(email).strip().lower()

        with engine.begin() as conn:

            # Check existing user
            result = conn.execute(
                text("""
                    SELECT id
                    FROM users
                    WHERE LOWER(email) = :email
                """),
                {
                    "email": email
                }
            ).fetchone()

            if result:

                return False, "Email already exists."

            # Hash password
            hashed_password = hash_password(password)

            # Create customer account
            conn.execute(
                text("""
                    INSERT INTO users
                    (
                        full_name,
                        email,
                        phone,
                        password,
                        role
                    )
                    VALUES
                    (
                        :full_name,
                        :email,
                        :phone,
                        :password,
                        :role
                    )
                """),
                {
                    "full_name": full_name,
                    "email": email,
                    "phone": phone,
                    "password": hashed_password,
                    "role": "customer"
                }
            )

        return True, "Registration Successful!"

    except Exception as e:

        return False, str(e)


# ===================================================
# LOGIN USER
# ===================================================

def login_user(
    email,
    password
):

    try:

        email = str(email).strip().lower()

        with engine.connect() as conn:

            user = conn.execute(
                text("""
                    SELECT
                        id,
                        full_name,
                        email,
                        phone,
                        password,
                        role
                    FROM users
                    WHERE LOWER(email) = :email
                """),
                {
                    "email": email
                }
            ).mappings().fetchone()

            # User not found
            if user is None:

                return False, "User not found."

            # Verify password
            if verify_password(
                password,
                user["password"]
            ):

                return True, user

            return False, "Incorrect Password."

    except Exception as e:

        return False, str(e)


# ===================================================
# GET USER
# ===================================================

def get_user(user_id):

    try:

        if not user_id:
            return None

        with engine.connect() as conn:

            user = conn.execute(
                text("""
                    SELECT
                        id,
                        full_name,
                        email,
                        phone,
                        password,
                        role
                    FROM users
                    WHERE id = :id
                """),
                {
                    "id": user_id
                }
            ).mappings().fetchone()

            return user

    except Exception:

        return None


# ===================================================
# CHECK ADMIN USER
# ===================================================

def is_admin_user(user):

    if not user:
        return False

    try:

        # SQLAlchemy RowMapping / dictionary
        if hasattr(user, "get"):

            role = user.get("role")
            email = user.get("email")

        else:

            role = getattr(
                user,
                "role",
                None
            )

            email = getattr(
                user,
                "email",
                None
            )

        # Check role
        if role:

            if str(role).strip().lower() == "admin":

                return True

        # Optional ADMIN_EMAIL support
        admin_email = os.environ.get(
            "ADMIN_EMAIL",
            ""
        ).strip().lower()

        if (
            admin_email
            and email
            and str(email).strip().lower() == admin_email
        ):

            return True

        return False

    except Exception:

        return False


# ===================================================
# UPDATE PROFILE
# ===================================================

def update_profile(
    user_id,
    full_name,
    phone
):

    try:

        with engine.begin() as conn:

            conn.execute(
                text("""
                    UPDATE users
                    SET
                        full_name = :full_name,
                        phone = :phone
                    WHERE id = :id
                """),
                {
                    "full_name": full_name,
                    "phone": phone,
                    "id": user_id
                }
            )

        return True, "Profile Updated Successfully."

    except Exception as e:

        return False, str(e)


# ===================================================
# CHANGE PASSWORD
# ===================================================

def change_password(
    user_id,
    new_password
):

    try:

        hashed = hash_password(
            new_password
        )

        with engine.begin() as conn:

            conn.execute(
                text("""
                    UPDATE users
                    SET password = :password
                    WHERE id = :id
                """),
                {
                    "password": hashed,
                    "id": user_id
                }
            )

        return True, "Password Updated Successfully."

    except Exception as e:

        return False, str(e)


# ===================================================
# MAKE USER ADMIN
# ===================================================

def make_user_admin(email):

    try:

        email = str(email).strip().lower()

        with engine.begin() as conn:

            result = conn.execute(
                text("""
                    UPDATE users
                    SET role = 'admin'
                    WHERE LOWER(email) = :email
                """),
                {
                    "email": email
                }
            )

            if result.rowcount == 0:

                return False, "User not found."

        return True, "User is now an Admin."

    except Exception as e:

        return False, str(e)


# ===================================================
# REMOVE ADMIN ROLE
# ===================================================

def remove_admin_role(email):

    try:

        email = str(email).strip().lower()

        with engine.begin() as conn:

            result = conn.execute(
                text("""
                    UPDATE users
                    SET role = 'customer'
                    WHERE LOWER(email) = :email
                """),
                {
                    "email": email
                }
            )

            if result.rowcount == 0:

                return False, "User not found."

        return True, "Admin role removed."

    except Exception as e:

        return False, str(e)


# ===================================================
# TOTAL USERS
# ===================================================

def total_users():

    try:

        with engine.connect() as conn:

            total = conn.execute(
                text("""
                    SELECT COUNT(*)
                    FROM users
                """)
            ).scalar()

            return total

    except Exception:

        return 0


# ===================================================
# LOGOUT
# ===================================================

def logout():

    return True