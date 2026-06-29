
from app.embeddings.embeddings_model import get_embedding_model
from app.vector_store.qdrantdb_client import get_qdrant_client
from app.retriever.load_bm25 import bm25_retriever
from app.utils.logger import logger


COLLECTION_NAME = "stackoverflow_python"


def dense_search(
    query: str,
    top_k: int = 2
):

    client = get_qdrant_client()

    embedding_model = get_embedding_model()
    
    logger.info(f"USING MODEL ID: {id(embedding_model)}")

    query_embedding = embedding_model.encode_query(
        query
    )

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=top_k,
    ).points

    # return [
    #     {
    #         **hit.payload,
    #         "score": hit.score
    #     }
    #     for hit in results
    # ]
    
    dense_results = [
        {
            **hit.payload,
            "score": hit.score
        }
        for hit in results
    ]

    best_score = (
        dense_results[0]["score"]
        if dense_results
        else 0.0
    )

    return dense_results, best_score


def retrieve(
    query: str,
    top_k: int = 2
):

    logger.info(
        f"Hybrid retrieval started for query: {query}"
    )

    dense_results, best_score = dense_search(
        query=query,
        top_k=10
    )

    bm25_results = bm25_retriever.retrieve(
        query=query,
        top_k=10
    )

    merged = {}

    for chunk in bm25_results:

        question_id = chunk.get(
            "question_id"
        )

        if question_id is not None:
            merged[
                question_id
            ] = chunk

    for chunk in dense_results:

        question_id = chunk.get(
            "question_id"
        )

        if question_id is not None:
            merged[
                question_id
            ] = chunk

    final_results = list(
        merged.values()
    )[:top_k]

    logger.info(
        f"Retrieved {len(final_results)} chunks"
    )

    return {
    "chunks": final_results,
    "best_score": best_score
    }


# P = dense_search(
#     "What is the difference between green and blue?"
# )

# print(P[0]["score"] if P else "No Results")