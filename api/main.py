from flask import Flask, request, Response
from flask_cors import CORS
from file_utils.get_models import get_models
from llm.llama_manager import llm_question
from llm.api_chat_sources import api_chat_sources
from vector_db.api_embeddings import api_embeddings
from vector_db.process_files import process_files

app = Flask(__name__)
CORS(app)


@app.route("/api/get-models", methods=["GET"])
def get_model_files():
    list_of_models = get_models("models")
    return list_of_models


@app.route("/api/chat-llama")
def chat_llama():
    question = request.args.get("question")
    model_name = request.args.get("model_name")

    def generate():
        response = llm_question(question, model_name)
        for word in response.split():
            yield word + " "

    return Response(generate(), mimetype="text/plain")


@app.route("/api/upload-files", methods=["POST"])
def upload_files():
    upload_files = process_files(request)
    return upload_files


@app.route("/api/similar-embeddings", methods=["POST"])
def similar_embeddings():
    similar_embeddings = api_embeddings(request)
    return similar_embeddings


@app.route("/api/chat-sources")
def chat_similarity():
    req = api_chat_sources(request)

    def generate_similarity():
        for word in req.split():
            yield word + " "

    return Response(generate_similarity(), mimetype="text/plain")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
