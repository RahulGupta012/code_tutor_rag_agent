
from app.retriever.retriever import retrieve
from app.retriever.web_search_duck import search_web

from app.chat_history.chathistory import (
    add_message,
    get_history
)

from app.cache.cache_service import (
    get_cached_response,
    cache_response
)

from app.utils.logger import logger

from app.chains.rag_chain import generate_answer
import time


def answer_question(query: str):
    total_start = time.perf_counter()
    

    cache_time = 0
    retrieval_time = 0
    prompt_time = 0
    llm_time = 0
    web_time = 0

    cached_response = get_cached_response(query)
    
    
    if cached_response:
        logger.info("Cache HIT")
        return cached_response
    
    cache_time = time.perf_counter() - total_start
    logger.info(f"Cache Lookup      : {cache_time*1000:.1f} ms")


    logger.info("Cache MISS")

    history = get_history()

    # ---------------- Hybrid Retrieval ----------------
    retrieval_start = time.perf_counter()

    retrieval = retrieve(query)
    
    retrieval_time = time.perf_counter() - retrieval_start

    retrieved_chunks = retrieval["chunks"]
    best_score = retrieval["best_score"]

    logger.info(f"Best Dense Score: {best_score:.3f}")
    
    logger.info(f"Hybrid Retrieval  : {retrieval_time*1000:.1f} ms")


    # ---------------- Threshold ----------------
    THRESHOLD = 0.5

    if best_score < THRESHOLD:
        
        web_start = time.perf_counter()


        logger.info(
            f"Low confidence ({best_score:.3f}). Using Web Search."
        )

        web_chunks = search_web(query)

        retrieved_chunks.extend(web_chunks[:3])
        
        web_time = time.perf_counter() - web_start
        
        logger.info(f"Web Search        : {web_time:.2f} sec")

    else:

        logger.info(
            f"High confidence ({best_score:.3f}). Using Local KB."
        )
        
        logger.info("Web Search        : Skipped")


    # ---------------- LLM ----------------
    llm_start = time.perf_counter()
    print("=" * 80)
    print("Retrieved Chunks:", len(retrieved_chunks))
    print(retrieved_chunks[0] if retrieved_chunks else "EMPTY")
    print("=" * 80)
    
    answer = generate_answer(
        query=query,
        contexts=retrieved_chunks,
        history=history
    )
    llm_time = time.perf_counter() - llm_start
    
    logger.info(f"LLM Response      : {llm_time:.2f} sec")


    # ---------------- Sources ----------------
    sources = []

    seen = set()

    for chunk in retrieved_chunks:

        # Web citation
        if chunk.get("source") == "web":

            url = chunk.get("url")

            if url and url not in seen:

                seen.add(url)

                sources.append(
                    {
                        "type": "web",
                        "title": chunk.get("title"),
                        "url": url
                    }
                )

        # Local citation
        else:

            question_id = chunk.get("question_id")

            if question_id and question_id not in seen:

                seen.add(question_id)

                sources.append(
                    {
                        "type": "local",
                        "question_id": question_id,
                        "title": chunk.get("title")
                    }
                )

    # ---------------- Chat History ----------------
    add_message("user", query)
    add_message("assistant", answer)

    # ---------------- Response ----------------
    response = {
        "answer": answer,
        "sources": sources[:2]  # Limit to 2 sources
    }

    cache_response(
        query=query,
        response=response
    )
    
    total_time = time.perf_counter() - total_start
    
    logger.info(f"Total time to process Request     : {total_time:.2f} sec")

    return response


