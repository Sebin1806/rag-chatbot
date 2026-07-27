from app.database.database import SessionLocal
from app.database.crud import (
    save_message,
    load_history,
    delete_history
)


class MemoryService:

    @staticmethod
    def add_message(session_id, role, content):

        db = SessionLocal()

        try:
            save_message(
                db,
                session_id,
                role,
                content
            )

        finally:
            db.close()

    @staticmethod
    def get_history(session_id):

        db = SessionLocal()

        try:
            return load_history(
                db,
                session_id
            )

        finally:
            db.close()

    @staticmethod
    def clear_history(session_id):

        db = SessionLocal()

        try:
            delete_history(
                db,
                session_id
            )

        finally:
            db.close()