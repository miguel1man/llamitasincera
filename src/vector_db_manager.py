import datetime
from langchain.vectorstores import Chroma
from embedding_manager import set_embedding

COLECCTION = "collection"
DIRECTORY = "vector_database/chroma_1"


def start_vector_db():
    vector_db = Chroma(
        collection_name=COLECCTION,
        embedding_function=set_embedding(),
        persist_directory=DIRECTORY,
    )
    return vector_db
