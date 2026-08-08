from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from rag_backend.app.db.models import Document
from rag_backend.app.services.chunking_service import chunk_text
from rag_backend.app.services.embedding_service import embedding_service
from rag_backend.app.services.parser_service import extract_text
from rag_backend.app.vectorstore.qdrant import qdrant_service


ALLOWED_EXTENSIONS = {".pdf", ".txt"}
ALLOWED_CHUNKING_STRATEGIES = {"fixed", "recursive"}


class DocumentService:
    """Handle document ingestion and processing."""

    async def process_document(
        self,
        file: UploadFile,
        strategy: str,
        db: Session,
    ) -> dict[str, object]:

        if not file.filename:
            raise ValueError("Filename is required.")

        extension = Path(file.filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise ValueError(
                "Only PDF and TXT files are supported."
            )

        strategy = strategy.lower()

        if strategy not in ALLOWED_CHUNKING_STRATEGIES:
            raise ValueError(
                "Chunking strategy must be 'fixed' or 'recursive'."
            )

        temporary_file_path: str | None = None

        try:
            file_content = await file.read()

            if not file_content:
                raise ValueError(
                    "The uploaded file is empty."
                )

            with NamedTemporaryFile(
                suffix=extension,
                delete=False,
            ) as temporary_file:
                temporary_file.write(file_content)
                temporary_file_path = temporary_file.name

            # Extract text from PDF/TXT
            text = extract_text(temporary_file_path)

            if not text.strip():
                raise ValueError(
                    "The uploaded document contains no "
                    "extractable text."
                )

            # Create chunks
            chunks = chunk_text(
                text=text,
                strategy=strategy,
                chunk_size=500,
                overlap=50,
            )

            if not chunks:
                raise ValueError(
                    "No chunks could be created from the document."
                )

            # Create document ID
            document_id = str(uuid4())

            # Generate embeddings
            embeddings = embedding_service.generate_embeddings(
                chunks
            )

            # Store vectors in Qdrant
            chunks_stored = qdrant_service.store_chunks(
                embeddings=embeddings,
                chunks=chunks,
                document_id=document_id,
                filename=file.filename,
            )

            # Store document metadata in SQL database
            document = Document(
                id=document_id,
                filename=file.filename,
                file_type=extension,
                chunking_strategy=strategy,
                total_chunks=chunks_stored,
            )

            db.add(document)
            db.commit()
            db.refresh(document)

            return {
                "document_id": document_id,
                "filename": file.filename,
                "file_type": extension,
                "chunking_strategy": strategy,
                "text_length": len(text),
                "chunks_created": chunks_stored,
                "status": "success",
            }

        finally:
            # Delete temporary file after processing
            if temporary_file_path:
                temporary_path = Path(temporary_file_path)

                if temporary_path.exists():
                    temporary_path.unlink()


document_service = DocumentService()