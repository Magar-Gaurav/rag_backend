from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PayloadSchemaType,
    PointStruct,
    VectorParams,
)
from rag_backend.app.core.config import settings


COLLECTION_NAME = "documents"
VECTOR_SIZE = 384


class QdrantService:
    """Handle vector database operations using Qdrant."""

    def __init__(self) -> None:
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )

    def create_collection(self) -> None:
        """Create the document collection if it does not exist."""

        collections = self.client.get_collections()

        collection_names = [
            collection.name
            for collection in collections.collections
        ]

        if COLLECTION_NAME not in collection_names:
            self.client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=VECTOR_SIZE,
                    distance=Distance.COSINE,
                ),
            )

        self.client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="document_id",
            field_schema=PayloadSchemaType.KEYWORD,
        )
    def store_chunks(
        self,
        embeddings: list[list[float]],
        chunks: list[str],
        document_id: str,
        filename: str,
    ) -> int:
        """Store chunk embeddings and metadata in Qdrant."""

        if len(embeddings) != len(chunks):
            raise ValueError(
                "The number of embeddings must match "
                "the number of chunks."
            )

        points: list[PointStruct] = []

        for index, (embedding, chunk) in enumerate(
            zip(embeddings, chunks)
        ):
            point = PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload={
                    "document_id": document_id,
                    "filename": filename,
                    "chunk_index": index,
                    "text": chunk,
                },
            )

            points.append(point)

        self.client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )

        return len(points)

    def search(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[dict]:
        """Search Qdrant and remove duplicate chunk text."""
    
        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            limit=limit * 3,
            with_payload=True,
        )
    
        unique_results: list[dict] = []
        seen_text: set[str] = set()
    
        for point in results.points:
            payload = point.payload or {}
    
            text = payload.get("text", "").strip()
    
            if not text:
                continue
            
            # Avoid returning the same chunk multiple times
            if text in seen_text:
                continue
            
            seen_text.add(text)
    
            unique_results.append(
                {
                    "score": point.score,
                    "text": text,
                    "document_id": payload.get("document_id"),
                    "filename": payload.get("filename"),
                    "chunk_index": payload.get("chunk_index"),
                }
            )
    
            if len(unique_results) >= limit:
                break
            
        return unique_results
    def delete_document(self, document_id: str) -> None:
        """Delete all vector chunks belonging to a document."""

        self.client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                ]
            ),
        )
        """Delete the document collection."""
        self.client.delete_collection(
             collection_name=COLLECTION_NAME
        )

qdrant_service = QdrantService()
qdrant_service.create_collection()