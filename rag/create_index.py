import os

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec


load_dotenv()


PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME",
    "urbanwear-rag"
)


if not PINECONE_API_KEY:

    raise ValueError(
        "PINECONE_API_KEY is missing from .env"
    )


print("Connecting to Pinecone...")


pc = Pinecone(
    api_key=PINECONE_API_KEY
)


existing_indexes = [
    index["name"]
    for index in pc.list_indexes()
]


if INDEX_NAME in existing_indexes:

    print()
    print(
        f"Index '{INDEX_NAME}' already exists."
    )

else:

    print()
    print(
        f"Creating index '{INDEX_NAME}'..."
    )

    pc.create_index(
        name=INDEX_NAME,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

    print(
        "Index creation request sent successfully."
    )


print()
print("Waiting for index to become ready...")


import time


while True:

    description = pc.describe_index(
        INDEX_NAME
    )

    status = description.status

    print(
        "Index status:",
        status
    )

    if status["ready"]:

        break

    time.sleep(2)


print()
print("=" * 50)
print("PINECONE INDEX CREATED SUCCESSFULLY")
print("=" * 50)

print()
print(
    "Index name:",
    INDEX_NAME
)

print(
    "Dimension:",
    description.dimension
)

print(
    "Metric:",
    description.metric
)

print(
    "Host:",
    description.host
)

print()
print("Your Pinecone RAG database is ready.")