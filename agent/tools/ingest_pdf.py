import os
import sys
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database.sqlite_vector import SQLiteVectorDB

def ingest_pdf(pdf_path: str):
    """Parses a PDF and stores its vector chunks."""
    text_content = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text: text_content += text + "\n"
    except Exception as e:
        print(f"Ingest Error: {e}")
        return False

    if not text_content.strip(): return False

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_text(text_content)
    
    db = SQLiteVectorDB()
    for i, chunk in enumerate(chunks):
        db.insert_chunk(chunk, metadata=f'{{"source": "{os.path.basename(pdf_path)}", "idx": {i}}}')
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1: ingest_pdf(sys.argv[1])
