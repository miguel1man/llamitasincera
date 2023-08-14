from langchain.vectorstores import Chroma
from embedding_manager import set_embedding
from vector_db_manager import INDEX_NAME, INDEX_PATH

RESULTS = 2


def vector_db_query(
    query_text, collection=INDEX_NAME, directory=INDEX_PATH, results=RESULTS
):
    vectordb = Chroma(
        collection_name=collection,
        embedding_function=set_embedding(),
        persist_directory=directory,
    )

    docs = vectordb.similarity_search_with_score(query=query_text, k=results)
    return docs


question = vector_db_query("La filosofía es...")
print("answer:", question)
