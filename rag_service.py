from app.services.generation_service import GenerationService

class RAGService:
    def __init__(self):
        # Existing DB and Model setup...
        self.generation_service = GenerationService()

    async def answer_question(self, query: str):
        """
        The Full RAG Pipeline:
        1. Retrieve: Find relevant docs in Qdrant.
        2. Generate: Send query + context to LLM.
        """
        # 1. Retrieval Phase
        context_results = await self.search(query)
        
        if not context_results:
            return "No relevant official documents found to answer your query."
            
        # 2. Generation Phase
        final_answer = await self.generation_service.generate_response(query, context_results)
        
        return {
            "answer": final_answer,
            "sources": [res['metadata'] for res in context_results] # Transparency principle
        }