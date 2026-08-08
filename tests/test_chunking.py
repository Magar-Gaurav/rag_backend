import pytest

from rag_backend.app.services.chunking_service import chunk_text


sample_text = """
Our company provides 15 days of annual leave to employees.

Working hours are from 9 AM to 5 PM.

Employees should submit leave requests in advance.

The company also provides sick leave according to its policies.
"""


def test_fixed_chunking() -> None:
    """Test fixed-size chunking."""

    chunks = chunk_text(
        sample_text,
        strategy="fixed",
        chunk_size=100,
        overlap=20,
    )

    assert len(chunks) > 0
    assert all(chunk.strip() for chunk in chunks)
    assert all(len(chunk) <= 100 for chunk in chunks)


def test_recursive_chunking() -> None:
    """Test recursive chunking."""

    chunks = chunk_text(
        sample_text,
        strategy="recursive",
        chunk_size=100,
        overlap=20,
    )

    assert len(chunks) > 0
    assert all(chunk.strip() for chunk in chunks)
    assert all(len(chunk) <= 100 for chunk in chunks)


def test_invalid_strategy() -> None:
    """Test that an invalid chunking strategy raises ValueError."""

    with pytest.raises(ValueError, match="Invalid chunking strategy"):
        chunk_text(
            sample_text,
            strategy="invalid",
        )


def test_fixed_chunking_with_no_overlap() -> None:
    """Test fixed-size chunking without overlap."""

    chunks = chunk_text(
        sample_text,
        strategy="fixed",
        chunk_size=100,
        overlap=0,
    )

    assert len(chunks) > 0
    assert all(len(chunk) <= 100 for chunk in chunks)


def test_invalid_chunk_size() -> None:
    """Test that an invalid chunk size raises ValueError."""

    with pytest.raises(ValueError, match="chunk_size"):
        chunk_text(
            sample_text,
            strategy="fixed",
            chunk_size=0,
            overlap=0,
        )


def test_invalid_overlap() -> None:
    """Test that overlap cannot be greater than or equal to chunk size."""

    with pytest.raises(ValueError, match="overlap"):
        chunk_text(
            sample_text,
            strategy="fixed",
            chunk_size=100,
            overlap=100,
        )


def test_strategy_is_case_insensitive() -> None:
    """Test that chunking strategy is case-insensitive."""

    chunks = chunk_text(
        sample_text,
        strategy="FIXED",
        chunk_size=100,
        overlap=20,
    )

    assert len(chunks) > 0