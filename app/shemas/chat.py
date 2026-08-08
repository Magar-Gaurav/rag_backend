from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(
        ...,
        description="Unique conversation session ID.",
    )

    question: str = Field(
        ...,
        min_length=1,
        description="Question to ask about the uploaded documents.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of document chunks to retrieve.",
    )


class ChatSource(BaseModel):
    score: float
    text: str
    document_id: str | None = None
    filename: str | None = None
    chunk_index: int | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSource]