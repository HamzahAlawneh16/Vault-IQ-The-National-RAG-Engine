from qdrant_client.http import models as rest_models
import uuid

# Inside VectorDBClient class, add this method:

def upsert_documents(self, collection_name: str, chunks: List['DocumentChunk']):
    """
    Complexity: O(B) where B is batch size.
    Standardized 'Upsert' operation for idempotency.
    """
    points = []
    for chunk in chunks:
        points.append(rest_models.PointStruct(
            id=str(uuid.uuid4()), # Generating unique ID for each chunk
            vector=chunk.vector,
            payload={"content": chunk.content, "metadata": chunk.metadata}
        ))

    self.client.upsert(
        collection_name=collection_name,
        points=points
    )