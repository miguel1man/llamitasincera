import os
from flask import jsonify


def get_models(folder_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(current_dir))
    models_dir = os.path.join(parent_dir, folder_name)
    list_of_models = [
        filename for filename in os.listdir(models_dir) if filename.endswith(".bin")
    ]
    return jsonify(list_of_models)
