import json
import os
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from file_utils.get_models import get_models
from llm.llama_manager import llm_question, llm_vector_similarity
from vector_db.process_files import process_files
from vector_db.requests_db import vector_db_query

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
    response = process_files(request)
    return response


@app.route("/api/similar-embeddings", methods=["POST"])
def similar_embeddings():
    req = request.json
    question_id = req["id"]
    question_text = req["question"]

    responses = vector_db_query(question_text)

    unique_responses = set()
    response_list = []

    for doc, score in responses:
        res_dict = {"text": doc.page_content, "metadata": doc.metadata, "score": score}
        res_json = json.dumps(res_dict, sort_keys=True)

        if res_json not in unique_responses:
            unique_responses.add(res_json)
            response_list.append(res_dict)

    response_with_id = {"id": question_id, "content": response_list}

    return jsonify(response_with_id)


@app.route("/api/chat-sources")
def chat_similarity():
    question = request.args.get("question")
    model_name = request.args.get("model_name")
    answer_db = vector_db_query(question)
    unique_responses = set()
    answer_data = []

    for doc, score in answer_db:
        res_dict = {"text": doc.page_content, "metadata": doc.metadata, "score": score}
        res_json = json.dumps(res_dict, sort_keys=True)

        if res_json not in unique_responses:
            unique_responses.add(res_json)
            answer_data.append(res_dict)

    # print("answer_data:", answer_data)
    # print("model_name:", model_name)
    def generate_similarity():
        response = llm_vector_similarity(question, answer_data, model_name)
        for word in response.split():
            yield word + " "

    return Response(generate_similarity(), mimetype="text/plain")


if __name__ == "__main__":
    app.run(port=6757, debug=True)
