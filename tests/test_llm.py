from rag_backend.app.services.llm_service import generate_answer


def test_llm_generation() -> None:
    answer = generate_answer(
        question="What is Machine Learning?",
        context=(
            "Machine Learning is a subset of Artificial Intelligence "
            "that enables systems to learn patterns from data."
        ),
        history=[],
    )

    assert isinstance(answer, str)
    assert len(answer) > 0