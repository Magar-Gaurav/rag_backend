from fastapi import APIRouter, HTTPException

from rag_backend.app.shemas.chat import ChatRequest, ChatResponse
from rag_backend.app.services.rag_service import rag_service


router = APIRouter(
    prefix="/api/v1",
    tags=["Chat"],
)


@router.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(request: ChatRequest) -> ChatResponse:
    """Answer a question using the uploaded documents."""

    try:
        result = rag_service.answer_question(
            session_id=request.session_id,
            question=request.question,
            top_k=request.top_k,
        )

        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to answer question: {exc}",
        ) from exc