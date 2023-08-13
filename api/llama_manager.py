from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

template_data = """
Pregunta:
{question}
Respuesta: 
Responde en idioma español únicamente utilizando estos datos como respuesta, no inventes hechos, solo utiliza estos datos:
{answer_data}"""


def llama_manager(question, answer_data, template=template_data):
    try:
        prompt = PromptTemplate(
            template=template,
            input_variables=["answer_data", "question"],
        )

        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

        llm = LlamaCpp(
            callback_manager=callback_manager,
            max_tokens=4096,
            n_ctx=2048,
            model_path="models/orca-mini-7b.ggmlv3.q4_1.bin",
            temperature=0,
            verbose=True,
        )

        llm_chain = LLMChain(prompt=prompt, llm=llm)

        inputs = {
            "answer_data": answer_data,
            "question": question,
        }
        llm_chain.run(inputs)

    except Exception as e:
        print(f"Error on llm processing: {e}")


template_question = """
Pregunta:
{question}
Respuesta: 
Responde en idioma español."""


def llama_manager_question(question, template=template_question):
    try:
        prompt = PromptTemplate(
            template=template,
            input_variables=["question"],
        )

        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

        llm = LlamaCpp(
            callback_manager=callback_manager,
            max_tokens=4096,
            n_ctx=2048,
            model_path="models/orca-mini-7b.ggmlv3.q2_K.bin",
            temperature=0,
            verbose=True,
        )

        llm_chain = LLMChain(prompt=prompt, llm=llm)

        inputs = {
            "question": question,
        }
        return llm_chain.run(inputs)

    except Exception as e:
        print(f"Error on llm processing: {e}")


""" 
llama_manager_question(
    "Escribe 3 slogan para una app de IA llamada Llamita sincera, que es una app basada en el LLM llama y solo responde con datos que tú le has entrenado, por eso es sincera."
)
 """
