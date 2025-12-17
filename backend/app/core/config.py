import os
from dotenv import load_dotenv

# Path to the .env file in the 'backend' directory
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME: str = "SpecKit RAG Backend"
    PROJECT_VERSION: str = "1.0.0"

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY")
    QDRANT_URL: str = os.getenv("QDRANT_URL")
    NEON_DATABASE_URL: str = os.getenv("NEON_DATABASE_URL")
    
    QDRANT_COLLECTION_NAME: str = "book_docs"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"  # Sentence-transformers model
    GENERATIVE_MODEL: str = "gpt-3.5-turbo" # OpenAI chat model

settings = Settings()
