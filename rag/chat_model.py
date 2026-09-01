import os

from dotenv import load_dotenv
from google import genai

from rag.retriever import search_knowledge


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


if not GEMINI_API_KEY:

    raise ValueError(
        "GEMINI_API_KEY is missing from .env"
    )


# =========================================================
# GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


MODEL_NAME = "gemini-2.5-flash"


# =========================================================
# BUILD CONTEXT
# =========================================================

def build_context(results):

    if not results:

        return "No relevant information was found."


    context_parts = []


    for number, result in enumerate(
        results,
        start=1
    ):

        context_parts.append(

            f"""
SOURCE {number}
File: {result['source']}
Chunk: {result['chunk']}

{result['text']}
"""
        )


    return "\n".join(
        context_parts
    )


# =========================================================
# ASK GEMINI
# =========================================================

def ask_gemini(
    question,
    top_k=5
):

    # -----------------------------------------------------
    # SEARCH PINECONE
    # -----------------------------------------------------

    results = search_knowledge(
        question,
        top_k=top_k
    )


    # -----------------------------------------------------
    # BUILD CONTEXT
    # -----------------------------------------------------

    context = build_context(
        results
    )


    # -----------------------------------------------------
    # SYSTEM INSTRUCTIONS
    # -----------------------------------------------------

    prompt = f"""
You are the AI shopping assistant for UrbanWear,
an online clothing store for men, women, kids,
and unisex customers.

Your job is to answer customer questions using
the provided knowledge base.

IMPORTANT RULES:

1. Use the knowledge base as your primary source.

2. Do not invent information that is not supported
   by the knowledge base.

3. If the answer cannot be found in the knowledge
   base, clearly say that you don't have that
   information.

4. Never pretend that you know a policy, product
   detail, shipping rule, return rule, or other
   store information when it is not present in
   the knowledge base.

5. Keep answers helpful, natural, and concise.

6. You are a clothing-store shopping assistant,
   so speak professionally and warmly.

7. If the customer asks about something unrelated
   to UrbanWear, politely explain that you can help
   with UrbanWear products, policies, shipping,
   returns, sizing, and shopping questions.

KNOWLEDGE BASE:

{context}

CUSTOMER QUESTION:

{question}

Now provide the best answer based only on the
available knowledge.
"""


    # -----------------------------------------------------
    # GENERATE ANSWER
    # -----------------------------------------------------

    response = client.models.generate_content(

        model=MODEL_NAME,

        contents=prompt

    )


    answer = response.text


    # -----------------------------------------------------
    # RETURN ANSWER + SOURCES
    # -----------------------------------------------------

    sources = []


    for result in results:

        source_name = result["source"]


        if source_name not in sources:

            sources.append(
                source_name
            )


    return {

        "answer": answer,

        "sources": sources

    }


# =========================================================
# TERMINAL TEST
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("URBANWEAR AI CHATBOT TEST")
    print("=" * 60)


    question = input(
        "\nAsk UrbanWear AI: "
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


    result = ask_gemini(
        question
    )


    print()
    print("-" * 60)
    print("AI ANSWER")
    print("-" * 60)

    print()

    print(
        result["answer"]
    )


    print()
    print("-" * 60)
    print("SOURCES")
    print("-" * 60)


    if result["sources"]:

        for source in result["sources"]:

            print(
                f"- {source}"
            )

    else:

        print(
            "No sources found."
        )


    print()
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)