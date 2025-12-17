from sqlalchemy.orm import Session
from . import models

def create_chat_history_entry(db: Session, session_id: str, role: str, message: str) -> models.ChatHistory:
    """
    Creates and saves a new chat history entry to the database.
    """
    db_entry = models.ChatHistory(session_id=session_id, role=role, message=message)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

def get_chat_history(db: Session, session_id: str) -> list[models.ChatHistory]:
    """
    Retrieves the full chat history for a given session_id, ordered by timestamp.
    """
    return db.query(models.ChatHistory).filter(models.ChatHistory.session_id == session_id).order_by(models.ChatHistory.timestamp).all()
