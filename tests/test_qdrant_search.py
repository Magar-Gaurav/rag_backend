from rag_backend.app.services.embedding_service import embedding_service
from rag_backend.app.vectorstore.qdrant import qdrant_service


def test_qdrant_search() -> None:
    query = "What is this document about?"

    query_embedding = embedding_service.generate_embeddings(
        [query]
    )[0]

    results = qdrant_service.search(
        query_embedding=query_embedding,
        limit=3,
    )

    assert isinstance(results, list)