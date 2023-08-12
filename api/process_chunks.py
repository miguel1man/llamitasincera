from embedding_manager import split_text_to_chunks
from vector_db_manager import start_vector_db

vector_db = start_vector_db()


def process_chunks(chunks):
    try:
        length = len(chunks)
        for i in range(length):
            chunk = chunks[i]["text"]
            file = chunks[i]["file"]
            header = chunks[i]["header"]

            texts = [chunk]
            print(f"\nlength characters: {len(texts[0])}")
            splits = split_text_to_chunks(texts[0])
            print("splits length:", len(splits))

            for split in splits:
                print("split length:", len(split))
                metadatas = [{"file": file, "header": header}]
                print(f"metadatas: {metadatas}")

                vector_db.add_texts(texts=[split], metadatas=metadatas)

        return True

    except Exception as e:
        print(f"Error while processing chunks: {e}")
        return False
