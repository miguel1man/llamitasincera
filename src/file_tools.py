import os


def scan_folder(folder_path):
    files = []

    for file in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, file)):
            type = os.path.splitext(file)[1].lstrip(".")
            files.append({"name": file, "type": type})

    return files
