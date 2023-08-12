from llama_manager import llama_manager
from vector_db_requests import vector_db_query


def chat_question(question):
    answers = vector_db_query(question)
    answer_data = ""

    # for answer in answers:
    #     print("metadata:\n", answer.metadata)

    answer_text = answers[0].page_content
    answer_header = answers[0].metadata["header"]

    answer_data = f"{answer_header}\n{answer_text}"
    print("\nquestion:\n", question)
    print("\nanswer_data:\n", answer_data)

    template = """
Lee esta pregunta separada entre 3 ticks:
```
{question}
```
Responde la pregunta anterior de manera concisa utilizando únicamente estos datos:
{answer_data}"""

    llama_manager(question=question, answer_data=answer_data, template=template)


chat_question("¿cuáles son las ventajas de la inteligencia artificial?")
