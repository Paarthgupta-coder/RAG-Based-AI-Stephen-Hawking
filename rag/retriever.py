#this converts ques -> vector and then searches nearest 5 chunks in chromaDB 
from sentence_transformers import SentenceTransformer
import chromadb

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "hawking_knowledge"

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_PATH)

def get_collection():
    try:
        return client.get_collection(name=COLLECTION_NAME)
    except:
        return None

def retrieve(query, n_results=5):
    collection = get_collection()

    if collection is None or collection.count() == 0:
        return []

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )

    chunks = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]

    retrieved = []

    for chunk, source in zip(chunks, sources):
        retrieved.append({
            "text": chunk,
            "source": source
        })

    return retrieved