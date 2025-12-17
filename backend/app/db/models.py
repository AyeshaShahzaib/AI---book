from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class IngestionLog(Base):
    __tablename__ = "ingestion_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, index=True) # e.g., "SUCCESS", "FAILURE"
    details = Column(Text, nullable=True)

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True) # To group messages by conversation
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    role = Column(String) # "user" or "assistant"
    message = Column(Text)
