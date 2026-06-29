from pydantic import BaseModel
from fastapi import FastAPI
from app.utils.logger import logger
from app.vector_store.qdrantdb_client import get_qdrant_client
from app.embeddings.embeddings_model import get_embedding_model
from app.retriever.load_bm25 import bm25_retriever
from contextlib import asynccontextmanager


from typing import Optional
from app.LLM.llm import get_llm



from app.services.query_service import answer_question
from fastapi.middleware.cors import CORSMiddleware



@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("=" * 60)
    logger.info("Starting Python Tutor RAG...")

    get_qdrant_client()
    logger.info("Qdrant Connected")

    get_embedding_model()
    logger.info(" Embedding Model Loaded")

    get_llm()
    logger.info(" Gemini Client Initialized")

    _ = bm25_retriever
    logger.info("BM25 Loaded")

    logger.info("Application Ready ")
    logger.info("=" * 60)

    yield

    logger.info("Shutting down...")


class Source(BaseModel):
    type: str
    title: Optional[str] = None
    question_id: Optional[int] = None
    answer_id: Optional[int] = None
    url: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]


class QueryRequest(BaseModel):
    question: str
    


app = FastAPI(
    title="Python Tutor RAG",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def root():

    return {
        "message": "Python Tutor RAG Running"
    }


@app.post(
    "/ask",
    response_model=QueryResponse
)
def ask(
    request: QueryRequest
):
    logger.info(f"Incoming question: {request.question}")
    
    result = answer_question(
        request.question
    )
    
    logger.info("Request completed successfully")

    return QueryResponse(
        answer=result["answer"],
        sources=result["sources"]
    )
    
@app.get("/health")
def health():

    try:

        client = get_qdrant_client()
        collections = client.get_collections()

        return {
            "status": "healthy",
            "vector_db": "connected",
            "collections_count": len(collections.collections)
        }

    except Exception as e:

        return {
            "status": "unhealthy",
            "vector_db": "disconnected",
            "error": str(e)
        }