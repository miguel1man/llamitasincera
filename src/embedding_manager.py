from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

models = {
    "mpnet": "paraphrase-multilingual-mpnet-base-v2",
    "minilm": "paraphrase-multilingual-MiniLM-L12-v2",
}


def set_embedding():
    embedding_fn = SentenceTransformerEmbeddings(model_name=models["minilm"])
    return embedding_fn


def get_embedding_from_sentence(sentence):
    model = SentenceTransformer(f"""sentence-transformers/{models["minilm"]}""")
    return model.encode(sentence)


def split_text_to_chunks(text):
    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
        chunks = splitter.split_text(text)
        return chunks

    except Exception as e:
        print(f"Error splitting texts to chunks: {e}")
