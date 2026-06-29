from rank_bm25 import BM25Okapi


class BM25Retriever:

    def __init__(self, documents):

        self.documents = documents

        self.tokenized_docs = [
            doc.page_content.lower().split()
            for doc in documents
        ]

        self.bm25 = BM25Okapi(
            self.tokenized_docs
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):

        tokenized_query = (
            query.lower().split()
        )

        scores = self.bm25.get_scores(
            tokenized_query
        )

        ranked_docs = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            {
                "content": doc.page_content,
                **doc.metadata
            }
            for doc, _
            in ranked_docs[:top_k]
        ]