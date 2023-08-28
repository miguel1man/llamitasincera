import mimetypes
import os
from flask import jsonify
from file_utils.file_tools import delete_files_in_folder
from file_utils.markdown_tools import process_markdown
from vector_db.manager_db import start_chroma_db
from vector_db.process_chunks import process_chunks_on_db


def process_files(request):
    try:
        FOLDER_PATH = "temp_uploads"

        if not os.path.exists(FOLDER_PATH):
            os.makedirs(FOLDER_PATH)

        files = request.files.getlist("files")
        response = []

        for file in files:
            try:
                file.save(os.path.join(FOLDER_PATH, file.filename))
                fileType = mimetypes.guess_type(file.filename)[0]
                # print(f"guess_type(file.filename): {fileType}")
                if fileType == "text/markdown":
                    chunks = process_markdown(os.path.join(FOLDER_PATH, file.filename))
                if fileType == "application/pdf":
                    print("PDF support coming soon")

                if process_chunks_on_db(chunks, start_chroma_db()):
                    response.append({"file": file.filename, "uploaded": True})
                else:
                    response.append({"file": file.filename, "uploaded": False}), 500

                delete_files_in_folder(FOLDER_PATH)

            except Exception as e:
                response.append({"file": file.filename, "uploaded": False}), 500
        # print(f"api response: {response}")
        return jsonify(response)

    except KeyError:
        return jsonify({"Missing parameter: files"}), 400

    except Exception as e:
        return jsonify({"Error uploading files to api": str(e)})
