from langchain_core.tools import tool
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b."""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b

@tool
def divide(a: int, b: int) -> float:
    """Divide a and b."""
    if b == 0:
        return 0.0
    return a / b

# ✅ TOOLS DEFINED FIRST (critical order!)
tools = [add, multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}

# ✅ NOW MODEL can use 'tools'
model_name = os.getenv("OLLAMA_MODEL", "qwen3:4b")
model = ChatOllama(model=model_name, temperature=0.1)

# ✅ 'tools' exists here - no NameError
model_with_tools = model.bind_tools(tools)
