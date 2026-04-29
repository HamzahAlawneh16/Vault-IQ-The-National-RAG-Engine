import logging
from typing import List, Dict
from fastapi import APIRouter, HTTPException, UploadFile, File, status

# Import Business Logic Services
from app.services.rag_service import RAGService
from app.services.ingestion_service import IngestionService
from app.services.document_processor import DocumentProcessor

# Standard Logging Setup
logger = logging.getLogger(__name__)

# Enterprise Versioning and Tagging
router = APIRouter(prefix="/v1", tags=["National RAG - API v1"])

# Dependency Injection (Singleton Pattern)
rag_service = RAGService()
ingestion_service = IngestionService()
doc_processor = DocumentProcessor()

@router.post("/ingest-text", status_code=status.HTTP_201_CREATED)
async def ingest_raw_text(payload: Dict[str, str]):
    """
    Leadership Principle: Invent and Simplify.
    Allows direct ingestion of raw text for quick data entries.
    """
    content = payload.get("content")
    source = payload.get("source", "manual_entry")
    
    if not content:
        raise HTTPException(status_code=400, detail="Content field is mandatory.")

    try:
        chunks = ingestion_service.process_raw_text(content, {"source": source})
        ingestion_service.upload_to_vector_db(chunks)
        return {"status": "success", "chunks_processed": len(chunks)}
    except Exception as e:
        logger.error(f"Ingestion failed: {str(e)}")
        raise HTTPException(status_code=500, detail="System failed to process raw text.")

@router.post("/upload-pdf", status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...)):
    """
    Leadership Principle: Insist on the Highest Standards.
    Handles official PDF document ingestion with automatic parsing and vectorization.
    """
    # Defensive Programming: Check file extension
    if not file.filename.lower().endswith(".pdf"):
        logger.warning(f"Unsupported file type attempted: {file.filename}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Unsupported File Type. Please upload a PDF."
        )

    try:
        # Read file into memory (Frugality: Avoid disk I/O for 8GB RAM systems)
        file_content = await file.read()
        
        # Offload to Document Processor
        success = await doc_processor.process_pdf(file_content, file.filename)
        
        if not success:
            raise Exception("Processing returned False status")

        return {
            "status": "success", 
            "filename": file.filename, 
            "detail": "Document successfully parsed, masked, and indexed."
        }
    except Exception as e:
        logger.error(f"Error processing PDF {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="An error occurred while processing the document."
        )

@router.post("/search", response_model=List[Dict])
async def search_vault(query: Dict[str, str]):
    """
    Leadership Principle: Customer Obsession.
    Main search entry point. Uses semantic retrieval to find relevant national docs.
    """
    user_prompt = query.get("prompt")
    if not user_prompt:
        raise HTTPException(status_code=400, detail="Search prompt is required.")

    try:
        # Perform Vector Search
        results = await rag_service.search(user_prompt)
        return results
    except Exception as e:
        logger.error(f"Search failure: {str(e)}")
        raise HTTPException(status_code=500, detail="Search engine is currently unavailable.")