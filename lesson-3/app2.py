import os
import gradio as gr
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

# Function to load all prompt templates dynamically
def load_prompts(folder="multiple_prompts"):
    prompts = {}
    for file in os.listdir(folder):
        if file.endswith(".txt"):
            path = os.path.join(folder, file)
            with open(path, "r") as f:
                prompts[file.replace(".txt", "").replace("_", " ").title()] = f.read()
    return prompts

# Load all prompt templates
prompts = load_prompts()

# Initialize Ollama model
llm = OllamaLLM(model="qwen3:4b")

# Function to apply selected prompt
def run_prompt(task, text):
    template = prompts[task]
    # Identify input variable name dynamically
    if "{sentence}" in template:
        input_var = "sentence"
    else:
        input_var = "text"

    prompt = PromptTemplate(input_variables=[input_var], template=template)
    return llm.invoke(prompt.format(**{input_var: text}))

# Gradio UI
demo = gr.Interface(
    fn=run_prompt,
    inputs=[
        gr.Dropdown(list(prompts.keys()), label="Choose a Task"),
        gr.Textbox(label="Enter your text or sentence"),
    ],
    outputs="text",
    title="🧠 Smart Prompt Assistant",
    description="Experiment with tone rewriting, summarization, translation, sentiment analysis, and grammar correction — powered by Ollama & LangChain."
)

if __name__ == "__main__":
    demo.launch()
