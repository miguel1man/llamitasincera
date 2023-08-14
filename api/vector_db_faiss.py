import os
from langchain.vectorstores import FAISS
from embedding_manager import set_embedding

INDEX_NAME = "index_1"
INDEX_PATH = "vector_db/faiss_1"

texts_1 = ["La filosofía es rascarse cuando no se pica."]
texts_2 = ["El arte no tiene por qué entenderse a la primera."]
faiss_text = FAISS.from_texts(texts=texts_1, embedding=set_embedding())


def faiss_vector_db():
    if not os.path.exists(INDEX_PATH):
        os.makedirs(INDEX_PATH)
        faiss_text.save_local(
            folder_path=INDEX_PATH,
        )
        print(f"saved embeddings")
        return True
    else:
        local_db = FAISS.load_local(folder_path=INDEX_PATH, embeddings=set_embedding())
        local_db.merge_from(faiss_text)
        local_db.save_local(folder_path=INDEX_PATH)
        print(f"return db: {local_db}")
        return True


faiss_vector_db()
