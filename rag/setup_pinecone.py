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
        "PINECONE_API_KEY was not found in the .env file."
    )


print("Connecting to Pinecone...")


pc = Pinecone(
    api_key=PINECONE_API_KEY
)


existing_indexes = [
    index["name"]
    for index in pc.list_indexes()
]


print(
    "Existing indexes:",
    existing_indexes
)


if INDEX_NAME not in existing_indexes:

    print(
        f"Creating Pinecone index: {INDEX_NAME}"
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

    print("Index creation requested.")

else:

    print(
        f"Index '{INDEX_NAME}' already exists."
    )


print()
print("Connecting to the index...")


index = pc.Index(
    INDEX_NAME
)


print()
print("SUCCESS!")
print(
    "Index name:",
    INDEX_NAME
)


description = pc.describe_index(
    INDEX_NAME
)


print(
    "Index host:",
    description.host
)


print(
    "Index dimension:",
    description.dimension
)


print(
    "Index metric:",
    description.metric
)