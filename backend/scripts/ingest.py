import os
import glob
import re
from dotenv import load_dotenv
import tiktoken
from sentence_transformers import SentenceTransformer # Changed from google.generativeai
from qdrant_client import QdrantClient, models
import uuid

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Constants
DOCS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'docs'))
QDRANT_COLLECTION_NAME = "book_docs"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # Changed to sentence-transformers model name
TOKENIZER_MODEL = "cl100k_base"
MAX_TOKENS = 400
# all-MiniLM-L6-v2 produces 384-dimensional vectors
VECTOR_SIZE = 384 # Changed vector size

def get_markdown_files():
    """Find all markdown and mdx files in the docs directory."""
    md_files = glob.glob(os.path.join(DOCS_PATH, "**/*.md"), recursive=True)
    mdx_files = glob.glob(os.path.join(DOCS_PATH, "**/*.mdx"), recursive=True)
    return md_files + mdx_files

def read_file_content(file_path):
    """Read the content of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def chunk_text(text, tokenizer, max_tokens=MAX_TOKENS):
    """Split text into chunks of a maximum token size."""
    tokens = tokenizer.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i + max_tokens]
        chunks.append(tokenizer.decode(chunk_tokens))
    return chunks

def process_and_embed_files(files, embedding_model, qdrant_client, tokenizer): # Changed parameter
    """Processes, chunks, and embeds the content of markdown files, then upserts them to Qdrant."""
    all_points = []
    for file_path in files:
        print(f"Processing {file_path}...")
        content = read_file_content(file_path)
        if not content:
            continue
            
        chapter = os.path.splitext(os.path.basename(file_path))[0]

        # Remove frontmatter
        content = re.sub(r'---.*?---', '', content, flags=re.DOTALL)
        
        # Split by section headings
        sections = re.split(r'\n## ', content)
        
        current_section_title = "Introduction"
        
        for i, section_content in enumerate(sections):
            if i > 0:
                lines = section_content.split('\n')
                current_section_title = lines[0].strip() if lines else 'Untitled Section'
                text_to_chunk = '\n'.join(lines[1:])
            else:
                text_to_chunk = section_content

            if not text_to_chunk.strip():
                continue

            chunks = chunk_text(text_to_chunk, tokenizer)
            
            for chunk in chunks:
                if not chunk.strip():
                    continue

                metadata = {
                    "source": "book",
                    "chapter": chapter,
                    "section": current_section_title,
                    "text": chunk
                }
                
                try:
                    # Generate embedding with sentence-transformers
                    embedding = embedding_model.encode(chunk).tolist() # Changed embedding call

                    all_points.append(models.PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embedding,
                        payload=metadata
                    ))
                except Exception as e:
                    print(f"Error embedding chunk: {e}")

    # Upsert all points to Qdrant in batches
    if all_points:
        batch_size = 100
        for i in range(0, len(all_points), batch_size):
            batch = all_points[i:i + batch_size]
            try:
                qdrant_client.upsert(
                    collection_name=QDRANT_COLLECTION_NAME,
                    points=batch,
                    wait=True
                )
                print(f"Upserted batch {i//batch_size + 1} with {len(batch)} points.")
            except Exception as e:
                print(f"Error upserting batch to Qdrant: {e}")
        print(f"Finished upserting a total of {len(all_points)} points to Qdrant.")

def main():
    """Main ingestion pipeline."""
    print("Starting ingestion pipeline with sentence-transformers embeddings...")
    # Initialize clients
    try:
        embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME) # Changed model initialization
        qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )
        tokenizer = tiktoken.get_encoding(TOKENIZER_MODEL)
    except Exception as e:
        print(f"Error initializing clients: {e}")
        print("Please ensure your .env file is set up correctly with QDRANT_URL, and QDRANT_API_KEY, and that `sentence-transformers` model is available.")
        return

    # Create collection if it doesn't exist
    try:
        qdrant_client.get_collection(collection_name=QDRANT_COLLECTION_NAME)
        print(f"Collection '{QDRANT_COLLECTION_NAME}' already exists.")
    except Exception:
        print(f"Collection '{QDRANT_COLLECTION_NAME}' not found. Creating new collection.")
        try:
            qdrant_client.recreate_collection(
                collection_name=QDRANT_COLLECTION_NAME,
                vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
            )
            print(f"Collection '{QDRANT_COLLECTION_NAME}' created successfully with vector size {VECTOR_SIZE}.")
        except Exception as e:
            print(f"Error creating Qdrant collection: {e}")
            return
            
    files = get_markdown_files()
    if not files:
        print("No markdown files found in the specified directory.")
        return

    process_and_embed_files(files, embedding_model, qdrant_client, tokenizer) # Changed parameter
    print("Ingestion pipeline finished.")

if __name__ == "__main__":
    main()

