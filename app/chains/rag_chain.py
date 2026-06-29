
# from app.retriever.retriever import retrieve
# from app.prompts.rag_prompt import build_prompt
# from app.LLM.llm import generate_response

# from app.chat_history.chathistory import (
#     add_message,
#     get_history
# )

# from app.cache.cache_service import (
#     get_cached_response,
#     cache_response
# )

# from app.utils.logger import logger


# def answer_question(query: str):


#     cached_response = get_cached_response(query)

#     if cached_response:

#         logger.info("Cache HIT")

#         return cached_response

#     logger.info("Cache MISS")



#     history = get_history()



#     retrieved_chunks = retrieve(query)



#     prompt = build_prompt(
#         query=query,
#         contexts=retrieved_chunks,
#         history=history
#     )


#     answer = generate_response(prompt)



#     add_message("user", query)
#     add_message("assistant", answer)



#     response = {
#         "answer": answer,
#         "sources": []
#     }


#     cache_response(
#         query=query,
#         response=response
#     )

#     return response

# # from langchain_core.output_parsers import StrOutputParser

# # from app.prompts.rag_prompt import rag_prompt
# # from app.LLM.llm import llm

# # rag_chain = (
# #     rag_prompt
# #     | llm
# #     | StrOutputParser()
# # )

from app.prompts.rag_prompt import build_prompt
from app.LLM.llm import generate_response


def generate_answer(
    query: str,
    contexts,
    history
):

    prompt = build_prompt(
        query=query,
        contexts=contexts,
        history=history
    )

    return generate_response(prompt)