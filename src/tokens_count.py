from transformers import AutoTokenizer
from embedding_manager import models

tokenizer = AutoTokenizer.from_pretrained(
    f"""sentence-transformers/{models["minilm"]}"""
)

tokens = tokenizer.encode("Texto de prueba")
print("tokens:", len(tokens))
