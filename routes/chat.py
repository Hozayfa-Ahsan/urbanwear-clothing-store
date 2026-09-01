from flask import Blueprint, request, jsonify

from rag.chat_model import ask_gemini


chat_bp = Blueprint(
    "chat",
    __name__
)


@chat_bp.route(
    "/api/chat",
    methods=["POST"]
)
def chat():

    data = request.get_json(
        silent=True
    )


    if not data:

        return jsonify({

            "success": False,

            "error": "Invalid request."

        }), 400


    question = data.get(
        "message",
        ""
    ).strip()


    if not question:

        return jsonify({

            "success": False,

            "error": "Please enter a message."

        }), 400


    try:

        result = ask_gemini(
            question
        )


        return jsonify({

            "success": True,

            "answer": result["answer"],

            "sources": result["sources"]

        })


    except Exception as error:

        print(
            "CHATBOT ERROR:",
            error
        )


        return jsonify({

            "success": False,

            "error": (
                "Sorry, the AI assistant "
                "is temporarily unavailable. "
                "Please try again."
            )

        }), 500