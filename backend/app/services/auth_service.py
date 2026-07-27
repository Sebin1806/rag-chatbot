from app.database.database import SessionLocal

from app.database.crud import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)

from app.utils.password import (
    hash_password,
    verify_password,
)

from app.utils.jwt import create_access_token


class AuthService:

    @staticmethod
    def register(username, email, password):

        db = SessionLocal()

        try:

            # Username already exists
            if get_user_by_username(db, username):
                return {
                    "success": False,
                    "message": "Username already exists."
                }

            # Email already exists
            if get_user_by_email(db, email):
                return {
                    "success": False,
                    "message": "Email already exists."
                }

            # Hash password
            hashed_password = hash_password(password)

            # Create user
            create_user(
                db,
                username,
                email,
                hashed_password
            )

            return {
                "success": True,
                "message": "User registered successfully."
            }

        finally:
            db.close()

    @staticmethod
    def login(email, password):

        db = SessionLocal()

        try:

            # Find user by email
            user = get_user_by_email(db, email)

            if not user:
                print("❌ User not found")
                return {
                    "success": False,
                    "message": "Invalid email or password."
                }

            print("========== LOGIN DEBUG ==========")
            print("Email Entered :", email)
            print("Password Entered :", password)
            print("Stored Hash :", user.password)

            valid = verify_password(
                password,
                user.password
            )

            print("Password Match :", valid)
            print("=================================")

            if not valid:
                return {
                    "success": False,
                    "message": "Invalid email or password."
                }

            access_token = create_access_token(
                {
                    "user_id": user.id,
                    "email": user.email
                }
            )

            return {
                "success": True,
                "access_token": access_token,
                "token_type": "bearer",
                "username": user.username
            }

        finally:
            db.close()