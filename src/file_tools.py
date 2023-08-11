import os
from markdown_tools import process_markdown
from process_chunks import process_chunks
from vector_db_manager import start_vector_db

vector_db = start_vector_db()


def scan_folder(folder_path):
    files = []

    for file in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file)):
            type = os.path.splitext(file)[1].lstrip(".")
            files.append({"name": file, "type": type})

    return files


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
