import json
from flask import jsonify
from vector_db.requests_db import vector_db_query


def api_embeddings(request):
    req = request.json
    question_id = req["id"]
    question_text = req["question"]

    responses = vector_db_query(question_text)
    # print(f"responses: /n{responses}")

    if len(responses) == 0:
        return jsonify({"id": question_id, "content": "No answers on DB."})

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
