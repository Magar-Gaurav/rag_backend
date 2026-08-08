from rag_backend.app.vectorstore.qdrant import qdrant_service
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from rag_backend.app.db.database import get_db
from rag_backend.app.services.document_service import document_service
from rag_backend.app.db.models import Document


router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"],
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    strategy: str = Query(
        default="recursive",
        description="Chunking strategy: fixed or recursive",
    ),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    """Upload and process a PDF or TXT document."""

    try:
        return await document_service.process_document(
            file=file,
            strategy=strategy,
            db=db,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {exc}",
        ) from exc
@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
) -> dict[str, object]:
    """Delete a document from SQL and Qdrant."""

    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    try:
        qdrant_service.delete_document(document_id)

        db.delete(document)
        db.commit()

        return {
            "document_id": document_id,
            "filename": document.filename,
            "status": "deleted",
        }

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete document: {exc}",
        ) from exc