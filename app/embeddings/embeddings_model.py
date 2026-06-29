from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.utils.logger import logger


@lru_cache(maxsize=1)
def get_embedding_model():

    logger.info("Loading BGE model into memory...")

    model = SentenceTransformer("BAAI/bge-base-en-v1.5")

    logger.info(f"Model id: {id(model)}")

    return model