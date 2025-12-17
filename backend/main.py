from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
# Load API keys from environment variables
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check if all required environment variables are set
if not all([QDRANT_URL, QDRANT_API_KEY, GROQ_API_KEY]):
    raise Exception("One or more environment variables are not set. Please check your .env file.")

# The name of the Qdrant collection for your AI book
COLLECTION_NAME = "ai_book"
LLM_MODEL = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# --- FastAPI APP INITIALIZATION ---
app = FastAPI(
    title="AI Book Q&A Backend",
    description="An API to answer questions about the AI book using a RAG architecture.",
    version="1.0.0",
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- DATABASE & AI SETUP ---
# Initialize the Qdrant client
client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# Initialize the HuggingFace embeddings model
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# Initialize the Qdrant vector store
vector_store = QdrantVectorStore(client=client, collection_name=COLLECTION_NAME, embeddings=embeddings)

# Initialize the Groq language model
llm = ChatGroq(api_key=GROQ_API_KEY, model_name=LLM_MODEL)


# --- API ENDPOINTS ---
class ChatRequest(BaseModel):
    """Request model for the /chat endpoint."""
    question: str
    selection: Optional[str] = None


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    This endpoint answers a user's question about the AI book.
    - If the user has selected text, it uses that text as context.
    - If no text is selected, it performs a similarity search in the Qdrant database to find relevant context.
    - It then uses a Groq language model to generate an answer based on the context.
    """
    try:
        context_text = ""
        # If user has selected text, use it as context
        if request.selection:
            print(f"📝 Using user-selected text as context: {request.selection[:50]}...")
            context_text = request.selection
        # Otherwise, search the vector database for context
        else:
            print(f"🔍 Searching for context for the question: {request.question}")
            docs = vector_store.similarity_search(request.question, k=3)
            context_text = "\n\n".join([doc.page_content for doc in docs])

        # If no context is found, return a default message
        if not context_text:
            return {"answer": "I could not find any relevant context to answer your question."}

        # Create the prompt template for the language model
        prompt_template = ChatPromptTemplate.from_template(
            """
            You are an expert AI tutor. Your task is to answer the user's question based *only* on the provided context.
            If the context does not contain the answer, state that you cannot answer the question from the given information.

            Context:
            {context}

            Question: {question}

            Answer:
            """
        )

        # Create the processing chain
        chain = prompt_template | llm

        # Invoke the chain to get the response
        response = chain.invoke({"context": context_text, "question": request.question})

        return {"answer": response.content}

    except Exception as e:
        print(f"❌ An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# --- APPLICATION RUN ---
if __name__ == "__main__":
    """
    This allows you to run the FastAPI application directly using `python main.py`.
    """
    uvicorn.run(app, host="0.0.0.0", port=8000)
