from flask import Flask, Response, request
from flask_cors import CORS
from llama_manager import llama_manager_question

app = Flask(__name__)
CORS(app)


@app.route("/api/chat-llama")
def chat_llama():
    question = request.args.get("question")

    def generate():
        response = llama_manager_question(question)
        for word in response.split():
            yield word + "\n"

    return Response(generate(), mimetype="text/plain")


if __name__ == "__main__":
    app.run(port=5001, debug=True)
