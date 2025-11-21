# Import ChatOllama wrapper for the Ollama LLM models
from langchain_ollama import ChatOllama

# Import LangChain prompt and chain components
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load the custom prompt template from file
with open("prompts/tone_prompt_template.txt", "r") as f:
    template = f.read()

# Initialize the local Qwen3:4b model (ensure name matches what is listed in 'ollama list')
llm = ChatOllama(model="qwen3:4b")

# Build the prompt template for the LLM
prompt = PromptTemplate(
    input_variables=["sentence"],
    template=template
)

# Connect the LLM and prompt with a chain
chain = LLMChain(llm=llm, prompt=prompt)

# Example input sentence for generation
user_sentence = "Let's finish the project quickly and impress our manager!"

# Run the chain with your input
result = chain.run(sentence=user_sentence)

# Print the result from the model
print(result)
