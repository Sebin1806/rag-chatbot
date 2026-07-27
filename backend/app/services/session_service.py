import uuid

from app.database.database import SessionLocal
from app.database.models import ChatSession


class SessionService:

    @staticmethod
    def create_session(title="New Chat"):

        db = SessionLocal()

        try:
            session = ChatSession(
                session_id=str(uuid.uuid4()),
                title=title
            )

            db.add(session)
            db.commit()
            db.refresh(session)

            return {
                "id": session.id,
                "session_id": session.session_id,
                "title": session.title
            }

        finally:
            db.close()

    @staticmethod
    def get_sessions():

        db = SessionLocal()

        try:

            sessions = (
                db.query(ChatSession)
                .order_by(ChatSession.created_at.desc())
                .all()
            )

            return [
                {
                    "id": s.id,
                    "session_id": s.session_id,
                    "title": s.title
                }
                for s in sessions
            ]

        finally:
            db.close()

    @staticmethod
    def delete_session(session_id):

        db = SessionLocal()

        try:

            db.query(ChatSession).filter(
                ChatSession.session_id == session_id
            ).delete()

            db.commit()

        finally:
            db.close()