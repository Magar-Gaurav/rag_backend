from rag_backend.app.vectorstore.qdrant import qdrant_service


if __name__ == "__main__":
    qdrant_service.create_collection()

    print("Qdrant collection initialized successfully.")