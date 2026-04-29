import uvicorn
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1_endpoints import router as api_v1
from app.core.config import settings

# 1. Leadership Principle: Operational Excellence (Logging Setup)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 2. Application Factory Strategy
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise-grade RAG system for National Documents. Focuses on Security, Privacy, and Scalability.",
    version="1.0.0",
    docs_url="/docs",  # Production docs endpoint
    redoc_url="/redoc"
)

# 3. Middleware for Global Error Handling (Amazon standard: Ownership)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Ensures that the system never crashes and returns a standard error format.
    """
    logger.error(f"Global error caught: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "An internal system error occurred. Our engineers are notified."},
    )

# 4. Standardized Routing Versioning
# We decouple the routes to app/api/v1_endpoints.py for better modularity
app.include_router(api_v1)

# 5. Monitoring Endpoints (Heartbeat)
@app.get("/health", tags=["Monitoring"])
async def health_check():
    """
    Used by load balancers and container orchestrators (K8s/Docker) 
    to verify service availability.
    """
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "infrastructure": "ready"
    }

# 6. Main Entry Point
if __name__ == "__main__":
    # In a Big Tech environment, we use uvicorn with worker scaling
    # 'reload=True' is only for development phase
    logger.info(f"Starting {settings.PROJECT_NAME} on port 8000...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)