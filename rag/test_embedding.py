import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")


if not api_key:

    raise ValueError(
        "GEMINI_API_KEY was not found in the .env file."
    )


print("Connecting to Gemini...")


embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=api_key
)


print("Creating test embedding...")


vector = embeddings.embed_query(
    "UrbanWear clothing store"
)


print()
print("SUCCESS!")
print(
    "Embedding dimension:",
    len(vector)
)
print(
    "First 5 values:",
    vector[:5]
)