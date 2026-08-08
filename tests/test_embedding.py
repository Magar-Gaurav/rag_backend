from rag_backend.app.services.embedding_service import embedding_service


def test_generate_embedding() -> None:
    text = "Employees receive 15 days of annual leave."

    embedding = embedding_service.generate_embedding(text)

    assert len(embedding) > 0
    assert all(isinstance(value, float) for value in embedding)