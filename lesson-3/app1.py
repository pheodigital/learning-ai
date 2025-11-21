import gradio as gr
# Import ChatOllama wrapper for the Ollama LLM models
from langchain_ollama import ChatOllama

# Import LangChain prompt and chain components
from langchain.prompts import PromptTemplate

# Load the custom prompt template from file
with open("prompts/tone_prompt_template_gradio.txt", "r") as f:
    template = f.read()

# Intialize the local Ollama model
llm = ChatOllama(model="qwen3:4b")

# Build the prompt template for the LLM
prompt = PromptTemplate(input_variables=["sentence", "tone"], template=template)

tones = ["formal", "casual", "friendly", "funny", "persuasive"]

def generate_tones(sentence):
  results = {}
  for tone in tones:
    formatted_prompt = prompt.format(sentence=sentence, tone=tone)
    response = llm.invoke(formatted_prompt)
    results[tone.capitalize()] = response
  return results

def gradio_interface(sentence):
    outputs = generate_tones(sentence)
    return [outputs[t] for t in outputs]

demo = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Textbox(label="Enter a sentence"),
    outputs=[gr.Textbox(label=t.capitalize()) for t in tones],
    title="🧠 Smart Prompting Assistant",
    description="Type a sentence to see how it sounds in different tones."
)

if __name__ == "__main__":
    demo.launch()