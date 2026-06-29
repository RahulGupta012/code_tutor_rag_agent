from app.utils.logger import logger

def build_prompt(
    query: str,
    contexts: list,
    history: list
):
    logger.info("Building prompt")

    context_text = "\n\n".join(
        str(chunk)
        for chunk in contexts
    )

    history_text = "\n".join(
        f"{msg['role']}: {msg['content']}"
        for msg in history
    )
    
    logger.info(f"Prompt length: {len(context_text)+len(history_text)+len(query)} characters")
    
    return f"""
You are an expert Python tutor.

Answer ONLY using the provided context and conversation history.

Rules:
1. Use the retrieved context as the primary source of truth.
2. Use chat history only to understand references such as "it", "that", "this", etc.
3. If the answer is not present in the context, say:
   "I could not find that information in the knowledge base."
4. Do not invent facts.
5. Explain concepts clearly with examples when possible.
6.Always answer in GitHub Markdown and Use fenced code blocks like ```python.



CHAT HISTORY:
{history_text}

CONTEXT:
{context_text}

QUESTION:
{query}

ANSWER:
"""

# from langchain_core.prompts import ChatPromptTemplate

# rag_prompt = ChatPromptTemplate.from_template(
# """
# You are an expert Python tutor.

# Answer ONLY using the provided context.

# If the answer is not present in the context, say:

# "I could not find that information in the knowledge base."

# CHAT HISTORY:
# {history}

# CONTEXT:
# {context}

# QUESTION:
# {question}

# ANSWER:
# """
# )
