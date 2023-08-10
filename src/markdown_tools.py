from file_tools import scan_folder
from langchain.text_splitter import MarkdownHeaderTextSplitter


def get_markdown_documents(folder_path):
    try:
        files = scan_folder(folder_path)
        markdown_documents = {}

        for file in files:
            file_path = folder_path + "/" + file["name"]
            with open(file_path) as f:
                text = f.read()
                markdown_documents[file["name"]] = {"text": text}

        return markdown_documents

    except Exception as e:
        print(f"Error scanning markdown: {e}")

    print("No markdown files found")


def markdown_splitter(md_docs):
    try:
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]

        md_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on
        )
        markdown_split_results = md_splitter.split_text(md_docs)

        return markdown_split_results

    except Exception as e:
        print(f"Error splitting: {e}")


def process_markdown(folder_path):
    try:
        processed_markdown = []
        files = scan_folder(folder_path)

        for file in files:
            print("Markdown to scan:", file["name"])
            md_docs = get_markdown_documents(folder_path)
            """ print("md_docs:", md_docs) """
            md_splits = markdown_splitter(md_docs[file["name"]]["text"])
            """ print("md_docs:", md_docs) """

            for md_split in md_splits:
                processed_markdown.append(
                    {
                        "text": md_split.page_content,
                        "header": md_split.metadata["Header 2"],
                        "file": file["name"],
                    }
                )

        return processed_markdown

    except Exception as e:
        print(f"Error while processing markdown: {e}")
