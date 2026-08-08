from typing import Callable


def fixed_size_chunking(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[str]:
    """Split text into fixed-size chunks with overlap."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be greater than or equal to 0 and less than chunk_size."
        )

    chunks: list[str] = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

def recursive_chunking(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[str]:
    """Split text recursively using paragraph, line, sentence, and word boundaries."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0.")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be greater than or equal to 0 "
            "and less than chunk_size."
        )

    separators = ["\n\n", "\n", ". ", " "]

    def recursive_split(
        current_text: str,
        separator_index: int,
    ) -> list[str]:

        current_text = current_text.strip()

        if not current_text:
            return []

        # Already small enough
        if len(current_text) <= chunk_size:
            return [current_text]

        # No separators left -> fixed-size fallback
        if separator_index >= len(separators):
            return fixed_size_chunking(
                current_text,
                chunk_size,
                overlap=0,
            )

        separator = separators[separator_index]

        pieces = [
            piece.strip()
            for piece in current_text.split(separator)
            if piece.strip()
        ]

        # Separator not useful
        if len(pieces) <= 1:
            return recursive_split(
                current_text,
                separator_index + 1,
            )

        chunks: list[str] = []
        current_chunk = ""

        for piece in pieces:

            # If this individual piece is larger than the limit,
            # recursively split it using the next separator.
            if len(piece) > chunk_size:

                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""

                chunks.extend(
                    recursive_split(
                        piece,
                        separator_index + 1,
                    )
                )

                continue

            candidate = (
                f"{current_chunk}{separator}{piece}"
                if current_chunk
                else piece
            )

            if len(candidate) <= chunk_size:
                current_chunk = candidate
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())

                current_chunk = piece

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    chunks = recursive_split(text, 0)

    # Add overlap between final chunks
    if overlap == 0:
        return chunks

    final_chunks: list[str] = []

    for index, chunk in enumerate(chunks):

        if index == 0:
            final_chunks.append(chunk)
            continue

        previous_chunk = chunks[index - 1]

        overlap_text = previous_chunk[-overlap:]

        combined = f"{overlap_text} {chunk}".strip()

        final_chunks.append(combined[:chunk_size])

    return final_chunks
def chunk_text(
    text: str,
    strategy: str,
    chunk_size: int = 500,
    overlap: int = 50,
) -> list[str]:
    """Chunk text using the selected strategy."""

    strategies: dict[str, Callable[..., list[str]]] = {
        "fixed": fixed_size_chunking,
        "recursive": recursive_chunking,
    }

    selected_strategy = strategies.get(strategy.lower())

    if selected_strategy is None:
        raise ValueError(
            "Invalid chunking strategy. "
            "Choose 'fixed' or 'recursive'."
        )

    return selected_strategy(
        text,
        chunk_size,
        overlap,
    )

