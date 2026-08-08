from rag_backend.app.db.database import Base, engine
from rag_backend.app.db import models


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    print("Database tables initialized successfully.")