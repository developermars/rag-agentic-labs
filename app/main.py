from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG System Backend",
    description="Production-ready backend for Retrieval-Augmented Generation system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HealthCheck(BaseModel):
    status: str
    service: str
    version: str

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class QueryResponse(BaseModel):
    query: str
    results: list
    metadata: Optional[dict] = None

# Health check endpoint
@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint for monitoring."""
    return HealthCheck(
        status="healthy",
        service="RAG System Backend",
        version="1.0.0"
    )

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "RAG System Backend is running"}

# Placeholder RAG query endpoint
@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Process RAG query.
    
    Args:
        request: Query request containing the search query
        
    Returns:
        QueryResponse with results
    """
    if not request.query or len(request.query.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    logger.info(f"Processing query: {request.query}")
    
    # Placeholder implementation
    return QueryResponse(
        query=request.query,
        results=[],
        metadata={"top_k": request.top_k}
    )

# Error handler
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled error: {str(exc)}")
    raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)