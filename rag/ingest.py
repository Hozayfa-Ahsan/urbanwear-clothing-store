import os
import time
import uuid

from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from pinecone import Pinecone


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
# PDF DIRECTORY
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)


# =========================================================
# GEMINI EMBEDDINGS
# =========================================================

print("Loading Gemini embedding model...")


embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=GEMINI_API_KEY
)


# =========================================================
# TEXT SPLITTER
# =========================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)


# =========================================================
# PINECONE
# =========================================================

print("Connecting to Pinecone...")


pc = Pinecone(
    api_key=PINECONE_API_KEY
)


index = pc.Index(
    INDEX_NAME
)


# =========================================================
# FIND PDF FILES
# =========================================================

pdf_files = [
    filename
    for filename in os.listdir(DATA_DIR)
    if filename.lower().endswith(".pdf")
]


if not pdf_files:

    raise FileNotFoundError(
        f"No PDF files found in: {DATA_DIR}"
    )


print()
print(
    f"Found {len(pdf_files)} PDF file(s)."
)


# =========================================================
# PROCESS PDFS
# =========================================================

total_chunks = 0

total_vectors_uploaded = 0


for filename in pdf_files:

    pdf_path = os.path.join(
        DATA_DIR,
        filename
    )


    print()
    print("=" * 60)

    print(
        f"Processing: {filename}"
    )

    print("=" * 60)


    # -----------------------------------------------------
    # READ PDF
    # -----------------------------------------------------

    reader = PdfReader(
        pdf_path
    )


    full_text = ""


    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text()


        if text:

            full_text += (
                f"\n\n"
                f"[Page {page_number}]\n"
                f"{text}"
            )


    if not full_text.strip():

        print(
            "WARNING: No extractable text found."
        )

        continue


    print(
        f"Extracted {len(full_text)} characters."
    )


    # -----------------------------------------------------
    # SPLIT TEXT
    # -----------------------------------------------------

    chunks = text_splitter.split_text(
        full_text
    )


    print(
        f"Created {len(chunks)} chunks."
    )


    total_chunks += len(chunks)


    # -----------------------------------------------------
    # CREATE AND UPLOAD EMBEDDINGS
    # -----------------------------------------------------

    print()
    print("Creating embeddings and uploading...")
    print()


    vectors = []


    for chunk_number, chunk in enumerate(
        chunks,
        start=1
    ):

        # -------------------------------------------------
        # RETRY EMBEDDING REQUEST
        # -------------------------------------------------

        max_retries = 5


        for attempt in range(
            max_retries
        ):

            try:

                vector = embeddings.embed_query(
                    chunk
                )

                break


            except Exception as error:

                error_text = str(
                    error
                )


                if (
                    "429" in error_text
                    or
                    "RESOURCE_EXHAUSTED"
                    in error_text
                ):

                    wait_time = (
                        10 * (attempt + 1)
                    )


                    print()
                    print(
                        "Gemini embedding quota "
                        "temporarily reached."
                    )

                    print(
                        f"Waiting {wait_time} seconds..."
                    )


                    time.sleep(
                        wait_time
                    )


                else:

                    raise


        else:

            raise RuntimeError(
                "Gemini embedding failed "
                "after multiple retries."
            )


        # -------------------------------------------------
        # CREATE VECTOR
        # -------------------------------------------------

        vector_id = str(
            uuid.uuid4()
        )


        vectors.append({

            "id": vector_id,

            "values": vector,

            "metadata": {

                "source": filename,

                "chunk": chunk_number,

                "text": chunk

            }

        })


        print(
            f"  Embedded "
            f"{chunk_number}/{len(chunks)}"
        )


        # -------------------------------------------------
        # SMALL DELAY
        # -------------------------------------------------

        time.sleep(
            3
        )


        # -------------------------------------------------
        # UPLOAD EVERY 10 VECTORS
        # -------------------------------------------------

        if (
            len(vectors) >= 10
            or
            chunk_number == len(chunks)
        ):

            print(
                f"  Uploading "
                f"{len(vectors)} vector(s)..."
            )


            index.upsert(
                vectors=vectors
            )


            total_vectors_uploaded += (
                len(vectors)
            )


            print(
                "  Upload successful."
            )


            vectors = []


    print()
    print(
        f"Finished: {filename}"
    )


# =========================================================
# FINAL RESULT
# =========================================================

print()
print("=" * 60)

print(
    "PDF INGESTION COMPLETE"
)

print("=" * 60)

print(
    f"PDF files found: {len(pdf_files)}"
)

print(
    f"Total chunks created: {total_chunks}"
)

print(
    f"Total vectors uploaded: "
    f"{total_vectors_uploaded}"
)


# =========================================================
# PINECONE STATISTICS
# =========================================================

print()
print(
    "Checking Pinecone..."
)


stats = index.describe_index_stats()


print()
print(
    "Total vectors currently in Pinecone:",
    stats.total_vector_count
)


print()
print(
    "RAG knowledge base is ready."
)