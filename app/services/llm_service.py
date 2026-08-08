import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


def generate_answer(
    question: str,
    context: str,
    history: list[dict[str, str]],
) -> str:
    """Generate a grounded answer using the retrieved document context."""

    conversation = ""

    for message in history:
        conversation += (
            f"{message['role']}: {message['content']}\n"
        )

    prompt = f"""
You are a document question-answering assistant.

Your job is to answer the user's question using ONLY the information
contained in the DOCUMENT CONTEXT below.

IMPORTANT RULES:

1. Use the document context as the only source of truth.
2. Do not use your general knowledge.
3. Do not add information that is not present in the document context.
4. If the answer is directly stated in the context, answer it directly.
5. If the context does not contain the answer, say:
   "I don't have enough information from the provided documents to answer that."
6. Keep the answer concise and clear.
7. Do not say that the information is unavailable when the answer is
   explicitly present in the context.

Conversation history:
{conversation}

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.0,
            },
        },
        timeout=120,
    )

    response.raise_for_status()

    result = response.json()

    return result["response"].strip()