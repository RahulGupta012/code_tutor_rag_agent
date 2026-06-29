import pickle

from app.retriever.bm25_retriver import (
    BM25Retriever
)

with open(
    "app/assets/processed/chunked_docs.pkl",
    "rb"
) as f:

    documents = pickle.load(f)

bm25_retriever = BM25Retriever(
    documents
)

