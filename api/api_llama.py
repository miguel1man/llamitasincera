from flask import Flask, Response, request
from flask_cors import CORS
from llama_manager import llama_manager_question
import time

app = Flask(__name__)
CORS(app)


@app.route("/api/llamacpp")
def stream_response():
    question = request.args.get("question")

    def generate():
        response = llama_manager_question(question)
        for word in response.split():
            yield word + "\n"
            time.sleep(1)

    return Response(generate(), mimetype="text/plain")


if __name__ == "__main__":
    app.run()
