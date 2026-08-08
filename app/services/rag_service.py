from rag_backend.app.services.embedding_service import embedding_service
from rag_backend.app.services.llm_service import generate_answer
from rag_backend.app.services.memory_service import memory_service
from rag_backend.app.vectorstore.qdrant import qdrant_service


class RAGService:
    """Handle retrieval-augmented question answering."""

    def answer_question(
        self,
        session_id: str,
        question: str,
        top_k: int = 5,
    ) -> dict[str, object]:

        question = question.strip()

        if not question:
            raise ValueError(
                "Question cannot be empty."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        # Get previous conversation
        history = memory_service.get_messages(
            session_id
        )

        # Convert question into an embedding
        query_embedding = embedding_service.generate_embedding(
            question
        )

        # Retrieve relevant document chunks
        search_results = qdrant_service.search(
            query_embedding=query_embedding,
            limit=top_k,
        )

        # Build context from retrieved chunks
        context_parts: list[str] = []

        for result in search_results:
            text = result.get("text", "")

            if text:
                context_parts.append(text)

        context = "\n\n".join(context_parts)

        # Generate answer using retrieved context
        answer = generate_answer(
            question=question,
            context=context,
            history=history,
        )

        # Save user message
        memory_service.save_message(
            session_id=session_id,
            role="user",
            content=question,
        )

        # Save assistant response
        memory_service.save_message(
            session_id=session_id,
            role="assistant",
            content=answer,
        )

        return {
            "answer": answer,
            "sources": search_results,
        }


rag_service = RAGService()