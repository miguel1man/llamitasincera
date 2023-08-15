import json
import os
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from file_tools import delete_files_in_folder
from llama_manager import llama_manager_question
from markdown_tools import process_markdown
from process_chunks import process_chunks
from vector_db_requests import vector_db_query

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
                chunks = process_markdown(os.path.join(FOLDER_PATH, file.filename))

                if process_chunks(chunks):
                    response.append({"file": file.filename, "uploaded": True})
                else:
                    response.append({"file": file.filename, "uploaded": False}), 500

                delete_files_in_folder(FOLDER_PATH)

            except Exception as e:
                response.append({"file": file.filename, "uploaded": False}), 500

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


if __name__ == "__main__":
    app.run(port=6757, debug=True)