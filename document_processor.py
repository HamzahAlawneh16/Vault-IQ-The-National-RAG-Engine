import fitz  # PyMuPDF
import logging
from typing import str
from app.services.ingestion_service import IngestionService

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    Leadership Principle: Dive Deep.
    Responsible for extracting high-quality text from official PDF documents.
    """
    def __init__(self):
        self.ingestion_service = IngestionService()

    async def process_pdf(self, file_bytes: bytes, filename: str):
        """
        Extracts text from PDF bytes and sends it to the Ingestion Pipeline.
        Complexity: O(P) where P is the number of pages.
        """
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            full_text = ""
            
            # Extract text page by page
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                full_text += page.get_text()
            
            if not full_text.strip():
                logger.warning(f"File {filename} appears to be empty or image-based.")
                return False

            # Metadata for traceability (Amazon Standard)
            metadata = {
                "source": filename,
                "total_pages": len(doc),
                "type": "official_document"
            }

            # Send to the Ingestion Factory
            chunks = self.ingestion_service.process_raw_text(full_text, metadata)
            self.ingestion_service.upload_to_vector_db(chunks)
            
            return True
        except Exception as e:
            logger.error(f"Failed to process PDF {filename}: {str(e)}")
            return False