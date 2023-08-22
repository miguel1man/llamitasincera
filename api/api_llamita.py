import json
import mimetypes
import os
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from file_tools import delete_files_in_folder
from llama_manager import llm_question, llm_vector_similarity
from markdown_tools import process_markdown
from process_chunks import process_chunks
from vector_db_requests import vector_db_query

app = Flask(__name__)
CORS(app)


@app.route("/api/get-models", methods=["GET"])
def get_model_files():
    model_files = [
        filename for filename in os.listdir("models") if filename.endswith(".bin")
    ]
    return jsonify(model_files)


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
    try:
        FOLDER_PATH = "temp_uploads"

        if not os.path.exists(FOLDER_PATH):
            os.makedirs(FOLDER_PATH)

        files = request.files.getlist("files")
        response = []

        for file in files:
            try:
                file.save(os.path.join(FOLDER_PATH, file.filename))
                fileType = mimetypes.guess_type(file.filename)[0]
                # print(f"guess_type(file.filename): {fileType}")
                if fileType == "text/markdown":
                    chunks = process_markdown(os.path.join(FOLDER_PATH, file.filename))
                if fileType == "application/pdf":
                    print("PDF support coming soon")

                if process_chunks(chunks):
                    response.append({"file": file.filename, "uploaded": True})
                else:
                    response.append({"file": file.filename, "uploaded": False}), 500

                delete_files_in_folder(FOLDER_PATH)

            except Exception as e:
                response.append({"file": file.filename, "uploaded": False}), 500
        # print(f"api response: {response}")
        return jsonify(response)

    except KeyError:
        return jsonify({"Missing parameter: files"}), 400

    except Exception as e:
        return jsonify({"Error uploading files to api": str(e)})


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
