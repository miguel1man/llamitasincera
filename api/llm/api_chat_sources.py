import json
from vector_db.requests_db import vector_db_query
from llm.llama_manager import llm_vector_similarity


def api_chat_sources(request):
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

    return llm_vector_similarity(question, answer_data, model_name)
