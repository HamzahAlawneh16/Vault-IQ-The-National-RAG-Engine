import logging
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.db.qdrant_client import VectorDBClient
from app.core.privacy_layer import PrivacyLayer
from app.models.pydantic_models import DocumentChunk
from sentence_transformers import SentenceTransformer
from app.core.config import settings

# Operational Excellence: Logging is mandatory for production systems
logger = logging.getLogger(__name__)

class IngestionService:
    """
    Leadership Principle: Invent and Simplify.
    This service transforms raw data into searchable vectors.
    """
    def __init__(self):
        self.db = VectorDBClient()
        self.privacy_filter = PrivacyLayer()
        # Initialize the embedding model (Frugality: CPU-optimized)
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        
        # Amazon-standard chunking: Overlap ensures context isn't lost at the edges
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len
        )

    def process_raw_text(self, raw_text: str, source_metadata: dict) -> List[DocumentChunk]:
        """
        Step 1: Clean & Mask
        Step 2: Split into Chunks
        Complexity: O(N) where N is text length.
        """
        # Secure the data first (Privacy by Design)
        masked_text = self.privacy_filter.mask_data(raw_text)
        
        # Break down large documents for better retrieval precision
        chunks = self.text_splitter.split_text(masked_text)
        
        processed_chunks = []
        for chunk in chunks:
            processed_chunks.append(DocumentChunk(
                content=chunk,
                metadata=source_metadata
            ))
        
        logger.info(f"Successfully processed {len(processed_chunks)} chunks.")
        return processed_chunks

    def upload_to_vector_db(self, chunks: List[DocumentChunk]):
        """
        Leadership Principle: Insist on the Highest Standards.
        Batch processing vectors for efficiency.
        """
        # 1. Generate Embeddings for all chunks (Vectorization)
        contents = [c.content for c in chunks]
        embeddings = self.model.encode(contents).tolist()
        
        # 2. Assign vectors to chunks
        for i, chunk in enumerate(chunks):
            chunk.vector = embeddings[i]
            
        # 3. Upsert to Qdrant (Handled via db client)
        # We will add an 'upsert' method to our VectorDBClient next
        self.db.upsert_documents("national_docs", chunks)
        logger.info("Batch upload to Qdrant completed.")