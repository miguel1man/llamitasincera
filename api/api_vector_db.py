from flask import Flask, request, jsonify
from vector_db_requests import vector_db_query
import json

app = Flask(__name__)


@app.route("/ask-db", methods=["POST"])
def ask_question():
    data = request.json
    question_id = data["id"]
    question_text = data["question"]

    responses = vector_db_query(question_text)

    unique_responses = set()
    response_list = []

    for res in responses:
        res_dict = {"text": res.page_content, "metadata": res.metadata}
        res_json = json.dumps(res_dict, sort_keys=True)

        if res_json not in unique_responses:
            unique_responses.add(res_json)
            response_list.append(res_dict)

    response_with_id = {"id": question_id, "response": response_list}

    return jsonify(response_with_id)


if __name__ == "__main__":
    app.run(debug=True)
