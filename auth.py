from sqlalchemy import text
from passlib.context import CryptContext
from database import engine

# ===================================================
# Password Hashing
# ===================================================

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)
def hash_password(password):
    password = str(password)

    # bcrypt max 72 bytes
    password = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")

    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    plain_password = str(plain_password)
    plain_password = plain_password.encode("utf-8")[:72].decode("utf-8", errors="ignore")

    return pwd_context.verify(plain_password, hashed_password)


# ===================================================
# Register User
# ===================================================

def register_user(full_name, email, phone, password):
    try:

        print("DEBUG PASSWORD:", repr(password))
        print("DEBUG LENGTH:", len(password.encode("utf-8")))

        hashed_password = hash_password(password)

        print("HASH CREATED SUCCESS")

        with engine.begin() as conn:

            # Check existing email
            result = conn.execute(
                text("""
                    SELECT id
                    FROM users
                    WHERE email = :email
                """),
                {"email": email}
            ).fetchone()

            if result:
                return False, "Email already exists."
            
            hashed_password = hash_password(str(password)[:72])
            conn.execute(
                text("""
                    INSERT INTO users
                    (
                        full_name,
                        email,
                        phone,
                        password
                    )
                    VALUES
                    (
                        :full_name,
                        :email,
                        :phone,
                        :password
                    )
                """),
                {
                    "full_name": full_name,
                    "email": email,
                    "phone": phone,
                    "password": hashed_password
                }
            )

        return True, "Registration Successful!"

    except Exception as e:
        return False, str(e)


# ===================================================
# Login User
# ===================================================

def login_user(email, password):

    try:
        with engine.connect() as conn:

            user = conn.execute(
                text("""
                    SELECT *
                    FROM users
                    WHERE email = :email
                """),
                {"email": email}
            ).mappings().fetchone()

            if user is None:
                return False, "User not found."

            if verify_password(password, user["password"]):
                return True, user

            return False, "Incorrect Password."

    except Exception as e:
        return False, str(e)


# ===================================================
# Get User
# ===================================================

def get_user(user_id):

    try:

        with engine.connect() as conn:

            user = conn.execute(
                text("""
                    SELECT *
                    FROM users
                    WHERE id = :id
                """),
                {"id": user_id}
            ).mappings().fetchone()

            return user

    except Exception:
        return None


# ===================================================
# Update Profile
# ===================================================

def update_profile(user_id, full_name, phone):

    try:

        with engine.begin() as conn:

            conn.execute(
                text("""
                    UPDATE users
                    SET
                        full_name = :full_name,
                        phone = :phone
                    WHERE
                        id = :id
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
# Change Password
# ===================================================

def change_password(user_id, new_password):

    try:

        hashed = hash_password(new_password)

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
# Total Users
# ===================================================

def total_users():

    try:

        with engine.connect() as conn:

            total = conn.execute(
                text("SELECT COUNT(*) FROM users")
            ).scalar()

            return total

    except Exception:
        return 0


# ===================================================
# Logout
# ===================================================

def logout():
    return True