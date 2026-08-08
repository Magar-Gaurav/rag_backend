from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Generate embeddings for text."""

    def __init__(self) -> None:
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def generate_embedding(self, text: str) -> list[float]:
        """Generate an embedding for a single text."""

        embedding = self.model.encode(text)

        return embedding.tolist()

    def generate_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate embeddings for multiple texts."""

        embeddings = self.model.encode(texts)

        return embeddings.tolist()


embedding_service = EmbeddingService()