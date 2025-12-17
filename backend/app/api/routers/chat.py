from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from openai import OpenAI
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from app.api.schemas import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.services.rag_service import RAGService
from app.api.deps import get_openai_client, get_embedding_model, get_qdrant_client
from app.db.database import get_db
from app.db import crud

router = APIRouter()

# Dependency for RAGService
def get_rag_service(
    openai_client: OpenAI = Depends(get_openai_client),
    embedding_model: SentenceTransformer = Depends(get_embedding_model),
    qdrant_client: QdrantClient = Depends(get_qdrant_client)
) -> RAGService:
    return RAGService(openai_client=openai_client, embedding_model=embedding_model, qdrant_client=qdrant_client)

# Dependency for ChatService
def get_chat_service(
    db: Session = Depends(get_db),
    rag_service: RAGService = Depends(get_rag_service)
) -> ChatService:
    return ChatService(db_session=db, rag_service=rag_service)


@router.post("/", response_model=ChatResponse)
async def handle_chat(
    chat_request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Main endpoint for handling chat requests.

    Receives a chat session and a list of messages, processes the request 
    through the ChatService, and returns the assistant's response.
    """
    return chat_service.process_chat(chat_request)

@router.get("/history/{session_id}", response_model=list[ChatResponse])
async def get_history(session_id: str, db: Session = Depends(get_db)):
    """
    Retrieves the chat history for a given session ID.
    """
    history = crud.get_chat_history(db, session_id=session_id)
    return [ChatResponse(role=item.role, content=item.message) for item in history]
