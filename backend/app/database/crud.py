from sqlalchemy.orm import Session

from app.database.models import ChatHistory, ChatSession

from app.database.models import User


def create_user(db, username, email, password):

    user = User(
        username=username,
        email=email,
        password=password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_by_email(db, email):

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

def get_user_by_username(db, username):

    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

def update_session_title(db, session_id, title):

    session = (
        db.query(ChatSession)
        .filter(ChatSession.session_id == session_id)
        .first()
    )

    if session:

        session.title = title

        db.commit()
def save_message(
    db: Session,
    session_id: str,
    role: str,
    message: str
):

    chat = ChatHistory(
        session_id=session_id,
        role=role,
        message=message
    )

    db.add(chat)
    db.commit()


def load_history(
    db: Session,
    session_id: str
):

    rows = (
        db.query(ChatHistory)
        .filter(ChatHistory.session_id == session_id)
        .order_by(ChatHistory.created_at)
        .all()
    )

    history = []

    for row in rows:

        history.append({
            "role": row.role,
            "content": row.message
        })

    return history


def delete_history(
    db: Session,
    session_id: str
):

    db.query(ChatHistory).filter(
        ChatHistory.session_id == session_id
    ).delete()

    db.commit()


def list_sessions(db: Session):

    rows = db.query(
        ChatHistory.session_id
    ).distinct().all()

    return [row[0] for row in rows]