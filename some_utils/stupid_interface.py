import logging

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import PromptTemplate
import gradio as gr

logger = logging.getLogger(__name__)

MODEL = "mistral:latest"


def query(instruction: str, contenuto: str) -> str:
    olly = OllamaLLM(model=MODEL)
    prompt = PromptTemplate.from_template(instruction)
    chain = prompt | olly
    return chain.invoke({"contenuto": contenuto})


def tab_00():
    with gr.TabItem("generic query"):
        with gr.Row():
            with gr.Column():
                instruction = gr.Textbox(
                    label="instruction",
                    value="""
                      Riassumi il contenuto del documento seguente.

                      Documento: {contenuto}""",
                    lines=6)
                contenuto = gr.Textbox(
                    value="",
                    lines=10)
                submit_btn = gr.Button("go")
            with gr.Column():
                response = gr.Textbox(
                    label="response",
                    lines=10)
        submit_btn.click(
            query,
            inputs=[instruction, contenuto],
            outputs=[response])


def launch_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# SLEC")
        with gr.Tabs():
            tab_00()

    demo.launch()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s [PID: %(process)d - %(filename)s %(funcName)s] - %(message)s",
        level=logging.INFO)
    logger.info("start")

    launch_interface()
