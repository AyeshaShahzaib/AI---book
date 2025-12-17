from openai import OpenAI
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from app.core.config import settings

def get_openai_client() -> OpenAI:
    return OpenAI(api_key=settings.OPENAI_API_KEY)

def get_embedding_model() -> SentenceTransformer:
    # Load the sentence-transformer model once globally
    if not hasattr(get_embedding_model, "model"):
        get_embedding_model.model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return get_embedding_model.model

def get_qdrant_client() -> QdrantClient:
    return QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY
    )
