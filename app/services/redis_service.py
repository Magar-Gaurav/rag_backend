import json

import redis

from rag_backend.app.core.config import settings


class RedisService:
    """Handle conversation memory using Redis."""

    def __init__(self) -> None:
        self.client = redis.from_url(
            settings.redis_url,
            decode_responses=True,
        )

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:
        """Save a conversation message."""

        key = f"chat:{session_id}"

        message = {
            "role": role,
            "content": content,
        }

        self.client.rpush(
            key,
            json.dumps(message),
        )

    def get_messages(
        self,
        session_id: str,
    ) -> list[dict[str, str]]:
        """Retrieve conversation history."""

        key = f"chat:{session_id}"

        messages = self.client.lrange(
            key,
            0,
            -1,
        )

        return [
            json.loads(message)
            for message in messages
        ]

    def clear_messages(
        self,
        session_id: str,
    ) -> None:
        """Clear conversation history."""

        key = f"chat:{session_id}"

        self.client.delete(key)


redis_service = RedisService()