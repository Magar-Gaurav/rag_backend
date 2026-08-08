# RAG Backend API

A document-based Question Answering backend built with FastAPI.

The system allows users to upload PDF/TXT documents, split the extracted text using different chunking strategies, generate embeddings, store them in Qdrant, retrieve relevant document chunks, and generate answers using a local LLM through Ollama.

It also supports Redis-based conversation memory for maintaining chat history.

---

## Features

- Upload PDF and TXT documents
- PDF/TXT text extraction
- Two selectable chunking strategies:
  - Fixed-size chunking
  - Recursive chunking
- Text embeddings using a sentence-transformer model
- Vector storage and similarity search using Qdrant
- Retrieval-Augmented Generation (RAG)
- Local LLM inference using Ollama
- Redis-based conversation memory
- Document deletion
- FastAPI Swagger/OpenAPI documentation
- Automated tests using pytest

---

## Architecture

```text
                ┌──────────────────┐
                │      Client      │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │     FastAPI      │
                │      API         │
                └────────┬─────────┘
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
      Document Upload             Chat API
             │                       │
             ▼                       ▼
       Text Extraction          Query Embedding
             │                       │
             ▼                       ▼
         Chunking                Qdrant Search
             │                       │
             ▼                       ▼
        Embeddings               Retrieved Context
             │                       │
             ▼                       ▼
          Qdrant ───────────────► Ollama
                                     │
                                     ▼
                                  Answer
                                     │
                                     ▼
                                   Redis
                              Conversation Memory
