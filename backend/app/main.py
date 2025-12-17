from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import chat

# Initialize the FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="A backend for a Retrieval-Augmented Generation (RAG) system."
)

# Include the chat router
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint for the backend.
    Provides a welcome message and basic information about the API.
    """
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.PROJECT_VERSION
    }
