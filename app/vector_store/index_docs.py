from app.vector_store.qdrantdb_client import get_qdrant_client
from app.embeddings.embeddings_model import get_embedding_model
from qdrant_client.models import PointStruct


from qdrant_client.models import (
    Distance,
    VectorParams
)



COLLECTION_NAME = "stackoverflow_python"


def create_collection():

    client = get_qdrant_client()
    collections = client.get_collections()

    existing = [
        c.name
        for c in collections.collections
    ]

    if COLLECTION_NAME not in existing:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE
            )
        )

        print("Collection Created")

    else:
        print("Collection Already Exists")
        

def index_documents(documents):

    points = []

    for idx, doc in enumerate(documents):
        
        embedding_model = get_embedding_model()
        client = get_qdrant_client()

        vector = embedding_model.encode(
            doc.page_content,
            normalize_embeddings=True
        )

        points.append(
            PointStruct(
                id=idx,
                vector=vector.tolist(),
                payload={
                    "content": doc.page_content,
                    **doc.metadata
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )