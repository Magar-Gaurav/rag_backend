from rag_backend.app.services.redis_service import redis_service


def test_redis_memory() -> None:
    session_id = "test-session"

    redis_service.clear_messages(session_id)

    redis_service.save_message(
        session_id=session_id,
        role="user",
        content="Hello",
    )

    redis_service.save_message(
        session_id=session_id,
        role="assistant",
        content="Hi! How can I help?",
    )

    messages = redis_service.get_messages(session_id)

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"

    redis_service.clear_messages(session_id)