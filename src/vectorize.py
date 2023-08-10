from markdown_tools import process_markdown
from process_chunks import process_chunks
from vector_db_manager import start_vector_db

vector_db = start_vector_db()


def vectorize(folder):
    try:
        chunks = process_markdown(folder)
        length = len(chunks)
        print(f"Total chunks: {length}")
        if process_chunks(chunks, vector_db):
            print("Chunks processed successfully")
        else:
            print("Error while processing chunks")

    except Exception as e:
        print(f"Error while vectorizing: {e}")


if __name__ == "__main__":
    vectorize("docs")
