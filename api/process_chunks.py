from embedding_manager import split_text_to_chunks
from vector_db_manager import start_chroma_db


def process_chunks(chunks):
    try:
        length = len(chunks)
        for i in range(length):
            chunk = chunks[i]["text"]
            file = chunks[i]["file"]
            header = chunks[i]["header"] if "header" in chunks[i] else None

            texts = [chunk]
            print(f"\nlength characters: {len(texts[0])}")
            splits = split_text_to_chunks(texts[0])
            print("splits length:", len(splits))

            for split in splits:
                print("split length:", len(split))
                metadatas = [{"file": file}]
                if header is not None:
                    metadatas[0]["header"] = header
                print(f"metadatas: {metadatas}")
                db = start_chroma_db()
                db.add_texts(texts=[split], metadatas=metadatas)

        return True

    except Exception as e:
        print(f"Error while processing chunks: {e}")
        return False
