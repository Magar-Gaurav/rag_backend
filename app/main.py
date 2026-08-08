from fastapi import FastAPI

from rag_backend.app.api.routes.documents import router as document_router
from rag_backend.app.api.routes.chat import router as chat_router


app = FastAPI(
    title="Conversational RAG Backend",
    description="Backend for document ingestion and conversational RAG.",
    version="1.0.0",
)

app.include_router(document_router)
app.include_router(chat_router)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}