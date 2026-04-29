from pydantic import BaseModel, Field
from typing import List, Optional

class DocumentChunk(BaseModel):
    """
    Standard schema for a document fragment.
    Ensures data consistency across the ingestion pipeline.
    """
    content: str = Field(..., description="The actual text content of the chunk")
    metadata: dict = Field(default_factory=dict, description="Source, page number, etc.")
    vector: Optional[List[float]] = None # Will be filled by the embedding model

class SearchResponse(BaseModel):
    """Schema for the final search result returned to the user."""
    score: float
    content: str
    metadata: dict