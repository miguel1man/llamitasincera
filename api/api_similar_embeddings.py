from flask import Flask, request, jsonify
from flask_cors import CORS
from vector_db_requests import vector_db_query
import json

app = Flask(__name__)
CORS(app)


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
    app.run(port=5003, debug=True)
