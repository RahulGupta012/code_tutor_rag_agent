from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200,
)

def chunk_documents(documents):

    final_docs = []

    for doc in documents:

        if len(doc.page_content) <= 3000:
            final_docs.append(doc)

        else:
            chunks = splitter.split_documents([doc])

            for idx, chunk in enumerate(chunks):

                chunk.metadata["chunk_id"] = idx
                chunk.metadata["parent_question_id"] = (
                    doc.metadata["question_id"]
                )

                final_docs.append(chunk)

    return final_docs