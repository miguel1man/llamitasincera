from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

template = """
Pregunta:
{question}
Respuesta: 
Responde en idioma español únicamente utilizando estos datos como respuesta, no inventes hechos, solo utiliza estos datos:
{answer_data}"""


def llama_manager(question, answer_data, template):
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


def llama_manager_question(question, template):
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
        llm_chain.run(inputs)

    except Exception as e:
        print(f"Error on llm processing: {e}")
