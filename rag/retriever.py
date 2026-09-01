import os

from dotenv import load_dotenv
from pinecone import Pinecone

from langchain_google_genai import GoogleGenerativeAIEmbeddings


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

INDEX_NAME = os.getenv(
    "PINECONE_INDEX_NAME",
    "urbanwear-rag"
)


# =========================================================
# VALIDATE CONFIGURATION
# =========================================================

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing from .env"
    )


if not PINECONE_API_KEY:
    raise ValueError(
        "PINECONE_API_KEY is missing from .env"
    )


# =========================================================
# GEMINI EMBEDDINGS
# =========================================================

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GEMINI_API_KEY
)


# =========================================================
# PINECONE CONNECTION
# =========================================================

pc = Pinecone(
    api_key=PINECONE_API_KEY
)

index = pc.Index(
    INDEX_NAME
)


# =========================================================
# SEARCH FUNCTION
# =========================================================

def search_knowledge(
    question,
    top_k=5
):

    question_vector = embeddings.embed_query(
        question
    )


    results = index.query(
        vector=question_vector,
        top_k=top_k,
        include_metadata=True
    )


    documents = []


    for match in results.matches:

        metadata = match.metadata or {}


        documents.append({

            "text": metadata.get(
                "text",
                ""
            ),

            "source": metadata.get(
                "source",
                "Unknown"
            ),

            "chunk": metadata.get(
                "chunk",
                ""
            ),

            "score": match.score

        })


    return documents


# =========================================================
# SIMPLE TERMINAL TEST
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("URBANWEAR RAG RETRIEVER TEST")
    print("=" * 60)


    question = input(
        "\nAsk a question about UrbanWear: "
    ).strip()


    if not question:

        print(
            "No question entered."
        )

        raise SystemExit


    print()
    print(
        "Searching knowledge base..."
    )


    results = search_knowledge(
        question,
        top_k=5
    )


    if not results:

        print()
        print(
            "No relevant information found."
        )

        raise SystemExit


    print()
    print(
        f"Found {len(results)} relevant results."
    )


    for number, result in enumerate(
        results,
        start=1
    ):

        print()
        print("-" * 60)

        print(
            f"RESULT {number}"
        )

        print(
            f"Source: {result['source']}"
        )

        print(
            f"Chunk: {result['chunk']}"
        )

        print(
            f"Similarity score: "
            f"{result['score']:.4f}"
        )

        print()

        print(
            result["text"]
        )


    print()
    print("=" * 60)
    print("RETRIEVER TEST COMPLETE")
    print("=" * 60)