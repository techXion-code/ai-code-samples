import chromadb
from sentence_transformers import SentenceTransformer

class ChromaRAG:
    def __init__(self):
        # Create a persistent Chroma database on disk
        self.client = chromadb.PersistentClient(path="./chroma_store")

        # Embedding model
        self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        # Start with a clean collection
        self._reset_collection()

    def _reset_collection(self):
        try:
            self.client.delete_collection("docs")
        except:
            pass
        self.collection = self.client.create_collection("docs")

    def build(self, chunks):
        """Create embeddings and store them in Chroma."""
        self._reset_collection()

        embeddings = self.embedder.encode(chunks).tolist()
        ids = [str(i) for i in range(len(chunks))]

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=chunks
        )

    def search(self, query, top_k=4):
        """Return the most relevant text chunks."""
        q_emb = self.embedder.encode([query]).tolist()[0]

        results = self.collection.query(
            query_embeddings=[q_emb],
            n_results=top_k
        )

        # Return list of documents (simple)
        return results["documents"][0]
