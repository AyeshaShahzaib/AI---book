import sys
import os

# This allows the script to find modules in the 'app' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.database import engine, Base
from app.db.models import IngestionLog, ChatHistory

def main():
    """
    Connects to the database and creates the necessary tables 
    based on the defined SQLAlchemy models.
    """
    print("Connecting to the database and creating tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables 'ingestion_logs' and 'chat_history' created successfully (if they didn't exist).")
    except Exception as e:
        print(f"An error occurred while creating tables: {e}")
        print("Please ensure your NEON_DATABASE_URL in the .env file is correct and the database is accessible.")

if __name__ == "__main__":
    main()
