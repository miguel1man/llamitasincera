import os
from langchain.text_splitter import MarkdownHeaderTextSplitter


def get_markdown_documents(file_path):
    try:
        md_docs = []
        with open(file_path) as f:
            text = f.read()
            file_name = os.path.basename(file_path)
            md_docs.append({"file": file_name, "text": text})
        print("markdown document:", md_docs)
        return md_docs

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
        print("markdown_split_results", markdown_split_results)

        return markdown_split_results

    except Exception as e:
        print(f"Error splitting: {e}")


def process_markdown(file_path):
    try:
        processed_markdown = []
        # print("File to scan:", file_path)
        md_docs = get_markdown_documents(file_path)
        # print("md text:", md_docs[0]["text"])
        md_splits = markdown_splitter(md_docs[0]["text"])

        for md_split in md_splits:
            processed_markdown.append(
                {
                    "text": md_split.page_content,
                    "header": md_split.metadata["Header 2"],
                    "file": md_docs[0]["file"],
                }
            )

        print("processed_markdown:", processed_markdown)
        return processed_markdown

    except Exception as e:
        print(f"Error while processing markdown: {e}")
