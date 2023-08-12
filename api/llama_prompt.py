from llama_manager import llama_manager

template_question = """Pregunta: {question}
Respuesta: Responde en idioma español."""

input_chat = "Escribe una lista con las diferencias entre moral y ética."

llama_manager(
    question=input_chat,
    template=template_question,
)
