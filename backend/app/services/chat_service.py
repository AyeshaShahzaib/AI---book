from sqlalchemy.orm import Session
from app.services.rag_service import RAGService
from app.db import crud
from app.api.schemas import ChatRequest, ChatResponse

class ChatService:
    def __init__(self, db_session: Session, rag_service: RAGService):
        self.db = db_session
        self.rag_service = rag_service

    def process_chat(self, chat_request: ChatRequest) -> ChatResponse:
        """
        Processes an incoming chat request:
        1. Saves the user's message to the database.
        2. Gets a response from the RAG service.
        3. Saves the assistant's response to the database.
        4. Returns the assistant's response.
        """
        # Get the latest user message from the request
        user_message = chat_request.messages[-1].content

        # Save user message to history
        crud.create_chat_history_entry(
            db=self.db,
            session_id=chat_request.session_id,
            role="user",
            message=user_message
        )

        # Get response from RAG service
        assistant_response_text = self.rag_service.query(user_message)

        # Save assistant response to history
        crud.create_chat_history_entry(
            db=self.db,
            session_id=chat_request.session_id,
            role="assistant",
            message=assistant_response_text
        )

        return ChatResponse(role="assistant", content=assistant_response_text)
