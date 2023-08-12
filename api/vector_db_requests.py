from langchain.vectorstores import Chroma
from embedding_manager import set_embedding
from vector_db_manager import COLECCTION, DIRECTORY

RESULTS = 1


def vector_db_query(
    query_text, collection=COLECCTION, directory=DIRECTORY, results=RESULTS
):
    vectordb = Chroma(
        collection_name=collection,
        embedding_function=set_embedding(),
        persist_directory=directory,
    )

    # docs = vectordb.similarity_search(query="", k=4, filter={"file": filter_text})
    docs = vectordb.similarity_search(query=query_text, k=results)
    return docs


# question = vector_db_query("¿qué es inteligencia artificial?")
# print("answer:", question)
