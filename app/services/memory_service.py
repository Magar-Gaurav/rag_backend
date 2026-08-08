from rag_backend.app.services.redis_service import redis_service


class MemoryService:
    """Handle conversation memory using Redis."""

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:
        """Save a message to conversation memory."""

        redis_service.save_message(
            session_id=session_id,
            role=role,
            content=content,
        )

    def get_messages(
        self,
        session_id: str,
    ) -> list[dict[str, str]]:
        """Retrieve conversation history."""

        return redis_service.get_messages(
            session_id=session_id,
        )

    def clear_messages(
        self,
        session_id: str,
    ) -> None:
        """Clear conversation history."""

        redis_service.clear_messages(
            session_id=session_id,
        )


memory_service = MemoryService()