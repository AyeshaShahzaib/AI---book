# SpecKit RAG Backend

This project is a backend for a Retrieval-Augmented Generation (RAG) system built with FastAPI. It uses Qdrant for vector storage, Neon Serverless Postgres for metadata, and OpenAI for embeddings and chat models.

## Setup

1.  **Install Dependencies:**
    Make sure you have Python 3.9+ installed. Then, from the `book/backend` directory, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Environment Variables:**
    In the `book/backend` directory, create a `.env` file (you can copy `.env.example`). This file should contain your Google API Key.

    Your `.env` file should look like this:
    ```
    OPENAI_API_KEY="your_openai_api_key"
    QDRANT_API_KEY="your_qdrant_api_key"
    QDRANT_URL="your_qdrant_cloud_url"
    NEON_DATABASE_URL="your_neon_postgres_connection_string"
    ```

3.  **Create Database Tables:**
    Run the script to create the necessary tables in your Neon Postgres database. Execute this command from the `book/backend` directory:
    ```bash
    python scripts/create_tables.py
    ```

4.  **Ingest Data:**
    Run the ingestion script to process the documentation files, generate embeddings, and store them in your Qdrant collection. This command should also be run from the `book/backend` directory.
    ```bash
    python scripts/ingest.py
    ```
    This may take a few minutes depending on the number of documents and your network speed.

## Running the Application

To run the FastAPI server, use uvicorn from the `book/backend` directory:
```bash
uvicorn app.main:app --reload
```
The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

The interactive API documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.

*   `POST /api/v1/chat/`: The main chat endpoint.
*   `GET /api/v1/chat/history/{session_id}`: Retrieve chat history for a session.

### Example Chat Request

You can use `curl` or any API client to interact with the chat endpoint.

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/chat/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "session_id": "my-test-session",
  "messages": [
    {
      "role": "user",
      "content": "What is the Turing Test?"
    }
  ]
}'
```
