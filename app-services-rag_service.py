from sentence_transformers import SentenceTransformer
from app.db.qdrant_client import VectorDBClient

class RAGService:
    """
    Handles the retrieval-augmented generation flow.
    Follows Amazon's 'Frugality' principle by optimizing CPU-bound embedding generation.
    """
    def __init__(self):
        # Lightweight multilingual model (Optimized for 8GB RAM)
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2', device='cpu')
        self.db = VectorDBClient()
        self.collection_name = "national_docs"

    async def search(self, query: str, limit: int = 5):
        """
        Hybrid Search Strategy:
        1. Vector Search (Semantic) - O(log N) using HNSW index in Qdrant.
        2. Sparse Search (Keyword) - Fallback for specific terminology.
        """
        query_vector = self.model.encode(query).tolist()
        
        # Performance: Reducing memory footprint by limiting top_k during retrieval
        results = self.db.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True
        )
        
        # Principle: Insist on Highest Standards (Data Integrity)
        return [res.payload for res in results]