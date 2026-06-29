from langchain_core.documents import Document

from app.ingestion.html_cleaning import clean_html


def create_documents(merged_df):

    documents = []

    for _, row in merged_df.iterrows():

        title = row["Title"]

        question = clean_html(row["Body_question"])

        answer = clean_html(row["Body_answer"])

        content = f"""
TITLE:
{title}

QUESTION:
{question}

ANSWER:
{answer}
"""

        metadata = {
            "question_id": int(row["Id_question"]),
            "answer_id": int(row["Id_answer"]),
            "question_score": int(row["Score_question"]),
            "answer_score": int(row["Score_answer"]),
            "source": "stackoverflow"
        }

        documents.append(
            Document(
                page_content=content,
                metadata=metadata
            )
        )

    return documents


