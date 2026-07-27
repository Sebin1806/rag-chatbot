from fastapi import APIRouter
from app.database.database import SessionLocal
from app.database.models import ChatHistory

from app.services.session_service import SessionService

router = APIRouter()


@router.post("/new")
async def new_chat():

    return SessionService.create_session()


@router.get("/")
async def get_chats():

    return SessionService.get_sessions()


@router.delete("/{session_id}")
async def delete_chat(session_id: str):

    SessionService.delete_session(session_id)

    return {
        "message": "Chat deleted successfully"
    }
@router.get("/{session_id}/history")
async def get_chat_history(session_id: str):

    db = SessionLocal()

    try:

        messages = (
            db.query(ChatHistory)
            .filter(ChatHistory.session_id == session_id)
            .order_by(ChatHistory.id.asc())
            .all()
        )

        return [
            {
                "role": msg.role,
                "content": msg.message
            }
            for msg in messages
        ]

    finally:
        db.close()