import os
import fitz  # <--- pymupdf
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "hawking_knowledge"
DATA_PATH = "data/sources"

def load_text_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def load_pdf_file(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def ingest():
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Connecting to ChromaDB...")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        client.delete_collection(COLLECTION_NAME)
        print("Old collection deleted.")
    except:
        pass

    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    files = os.listdir(DATA_PATH)
    if not files:
        print("No files found in data/sources. Add PDFs or .txt files there first.")
        return

    all_chunks = []
    all_ids = []
    all_metadata = []

    for filename in files:
        filepath = os.path.join(DATA_PATH, filename)
        print(f"Reading: {filename}")

        if filename.endswith(".pdf"):
            text = load_pdf_file(filepath)
        elif filename.endswith(".txt"):
            text = load_text_file(filepath)
        else:
            print(f"Skipping unsupported file: {filename}")
            continue

        chunks = chunk_text(text)
        print(f"  -> {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_ids.append(f"{filename}_chunk_{i}")
            all_metadata.append({"source": filename})

    print(f"\nEmbedding {len(all_chunks)} total chunks...")
    embeddings = model.encode(all_chunks, show_progress_bar=True).tolist()

    print("Storing in ChromaDB...")
    collection.add(
        documents=all_chunks,
        embeddings=embeddings,
        ids=all_ids,
        metadatas=all_metadata
    )

    print(f"\nDone! {len(all_chunks)} chunks stored in ChromaDB.")

if __name__ == "__main__":
    ingest()