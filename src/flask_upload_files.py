import os
from flask import Flask, jsonify, request
from markdown_tools import process_markdown
from process_chunks import process_chunks

app = Flask(__name__)


@app.route("/upload", methods=["POST"])
def process_markdown_route():
    try:
        file_path = request.json["file_path"]
        chunks = process_markdown(file_path)
        if process_chunks(chunks):
            file_name = os.path.basename(file_path)
            return jsonify(file_name)
        else:
            return jsonify({"error": "Error while processing chunks"}), 500
    except KeyError:
        return jsonify({"error": "Missing 'file_path' parameter"}), 400
    except Exception as e:
        return jsonify({"error on flask api": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
