from langchain.document_loaders import PyPDFLoader, DirectoryLoader


def scan_pdf_from_folder(folder_path):
    try:
        loader = DirectoryLoader(
            f"{folder_path}/", glob="*.pdf", loader_cls=PyPDFLoader
        )
        documents = loader.load()

        if not documents:
            print("No documents found")
            return []

    except Exception as e:
        print(f"Error while scanning local folder_path: {folder_path}\n{e}")
        return []

    return documents
