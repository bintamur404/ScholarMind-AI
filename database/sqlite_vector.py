import sqlite3
import sqlite_vec
import struct
from typing import List, Tuple
from langchain_google_genai import GoogleGenerativeAIEmbeddings

class SQLiteVectorDB:
    def __init__(self, db_path: str = "scholar_mind.db"):
        self.db_path = db_path
        # Use Google Gemini Embeddings (Verified models/gemini-embedding-001 is available)
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        self.vector_dim = 768  # Dimension for text-embedding-004
        self.init_db()

    def get_connection(self):
        """Creates a connection and loads the sqlite-vec extension."""
        conn = sqlite3.connect(self.db_path)
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)
        return conn

    def init_db(self):
        """Initializes the database schema with a virtual vector table."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create a virtual table for vectors (using vec0 extension)
        cursor.execute(f"CREATE VIRTUAL TABLE IF NOT EXISTS vec_items USING vec0(embedding float[{self.vector_dim}])")
        
        # Create a standard table for document metadata and text content
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                metadata TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def serialize_float32(self, vector: List[float]) -> bytes:
        """Serializes a list of floats into a tightly-packed bytes object for sqlite-vec."""
        return struct.pack(f"{len(vector)}f", *vector)

    def embed_text(self, text: str) -> List[float]:
        """Generates embedding for the given text."""
        return self.embeddings.embed_query(text)

    def insert_chunk(self, text: str, metadata: str = "{}"):
        """Inserts a text chunk and its vector into the database."""
        embedding = self.embed_text(text)
        embedding_bytes = self.serialize_float32(embedding)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Insert text and get row ID
        cursor.execute("INSERT INTO documents (text, metadata) VALUES (?, ?)", (text, metadata))
        doc_id = cursor.lastrowid
        
        # Insert vector mapping to the same ID
        cursor.execute("INSERT INTO vec_items (rowid, embedding) VALUES (?, ?)", (doc_id, embedding_bytes))
        
        conn.commit()
        conn.close()
        return doc_id

    def similarity_search(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """Performs a KNN search using vector similarity."""
        query_embedding = self.embed_text(query)
        query_bytes = self.serialize_float32(query_embedding)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Use MATCH operator for sqlite-vec KNN search
        cursor.execute(f"""
            SELECT 
                documents.text, 
                vec_items.distance
            FROM vec_items 
            JOIN documents ON vec_items.rowid = documents.id
            WHERE vec_items.embedding MATCH ? AND k = ?
            ORDER BY vec_items.distance ASC
        """, (query_bytes, top_k))
        
        results = cursor.fetchall()
        conn.close()
        return results
