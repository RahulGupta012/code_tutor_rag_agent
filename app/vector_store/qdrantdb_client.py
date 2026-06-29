from qdrant_client import QdrantClient
from functools import lru_cache
from dotenv import load_dotenv
from app.utils.logger import logger
import os

load_dotenv()

@lru_cache(maxsize=1)
def get_qdrant_client() -> QdrantClient:

    # host = os.getenv("QDRANT_HOST")
    # port = int(os.getenv("QDRANT_PORT"))
    
    host = "localhost"
    port = 6333

    logger.info("Initializing Qdrant client...")

    return QdrantClient(
        host=host,
        port=port
    )