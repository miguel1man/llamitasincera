import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from file_tools import delete_files_in_folder
from markdown_tools import process_markdown
from process_chunks import process_chunks

app = Flask(__name__)
CORS(app)


@app.route("/upload", methods=["POST"])
def process_markdown_route():
    try:
        FOLDER_PATH = "uploads"

        if not os.path.exists(FOLDER_PATH):
            os.makedirs(FOLDER_PATH)

        files = request.files.getlist("files")
        response = []

        for file in files:
            try:
                file.save(os.path.join(FOLDER_PATH, file.filename))
                chunks = process_markdown(os.path.join(FOLDER_PATH, file.filename))

                if process_chunks(chunks):
                    response.append({"file": file.filename, "uploaded": True})
                else:
                    response.append({"file": file.filename, "uploaded": False}), 500

                delete_files_in_folder(FOLDER_PATH)

            except Exception as e:
                response.append({"file": file.filename, "uploaded": False}), 500

        return jsonify(response)

    except KeyError:
        return jsonify({"error": "Missing 'files' parameter"}), 400

    except Exception as e:
        return jsonify({"error on upload api": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
