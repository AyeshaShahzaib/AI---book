from openai import OpenAI
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from app.core.config import settings

class RAGService:
    def __init__(self, openai_client: OpenAI, embedding_model: SentenceTransformer, qdrant_client: QdrantClient):
        self.openai_client = openai_client
        self.embedding_model = embedding_model
        self.qdrant_client = qdrant_client

    def query(self, query_text: str) -> str:
        """
        Performs a RAG query:
        1. Embeds the query text using sentence-transformers.
        2. Searches Qdrant for relevant context.
        3. Constructs a prompt with the context.
        4. Gets a response from an OpenAI chat model.
        """
        # 1. Create embedding for the query
        try:
            query_embedding = self.embedding_model.encode(query_text).tolist()
        except Exception as e:
            print(f"Error creating query embedding: {e}")
            return "Error: Could not process the query."

        # 2. Search for similar vectors in Qdrant
        try:
            search_result = self.qdrant_client.search(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                query_vector=query_embedding,
                limit=3,
                with_payload=True
            )
        except Exception as e:
            print(f"Error searching Qdrant: {e}")
            return "Error: Could not retrieve context from the knowledge base."

        # 3. Construct the context for the prompt
        context = "\n---\n".join([hit.payload['text'] for hit in search_result])

        if not context:
            return "I couldn't find any relevant information in the documentation to answer your question."

        # 4. Create the prompt
        prompt = f"""
        You are an expert assistant for the SpecKit Plus documentation.
        Please answer the user's question based on the following context from the project's book.
        Your answer should be clear, concise, and directly address the question.
        If the context does not contain the answer, state that you couldn't find a definitive answer in the provided documentation.

        Context from the book:
        ---
        {context}
        ---

        User's question:
        {query_text}
        """

        # 5. Get a response from the chat model
        try:
            chat_response = self.openai_client.chat.completions.create(
                model=settings.GENERATIVE_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful and precise assistant for the SpecKit Plus documentation."},
                    {"role": "user", "content": prompt}
                ]
            )
            return chat_response.choices[0].message.content
        except Exception as e:
            print(f"Error getting response from OpenAI chat model: {e}")
            return "Error: Could not generate a response."
