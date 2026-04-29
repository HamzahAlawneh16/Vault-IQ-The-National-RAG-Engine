import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models
import os

# Initialize logging for observability
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorDBClient:
    """
    Leadership Principle: Invent and Simplify.
    Encapsulates Qdrant operations to provide a clean interface for the service layer.
    """
    def __init__(self):
        self.host = os.getenv("QDRANT_HOST", "localhost")
        self.port = 6333
        self.client = QdrantClient(host=self.host, port=self.port)
        logger.info(f"Connected to Qdrant at {self.host}:{self.port}")

    def create_collection(self, collection_name: str, vector_size: int):
        """
        Ensures idempotency by checking if the collection exists before creating it.
        Complexity: O(1) for check, O(N) for creation metadata.
        """
        if not self.client.collection_exists(collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size, 
                    distance=models.Distance.COSINE
                )
            )
            logger.info(f"Collection {collection_name} created.")