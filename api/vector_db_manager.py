from langchain.vectorstores import Chroma
from embedding_manager import set_embedding

INDEX_NAME = "index_1"
INDEX_PATH = "vector_db/chroma_1"


def start_vector_db():
    vector_db = Chroma(
        collection_name=INDEX_NAME,
        embedding_function=set_embedding(),
        persist_directory=INDEX_PATH,
    )
    return vector_db
