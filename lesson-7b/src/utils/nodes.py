from langchain_core.messages import SystemMessage, ToolMessage
from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv
from .tools import tools, tools_by_name, model_with_tools  # ✅ Import ALL needed
from .state import MessagesState

load_dotenv()

def llm_call(state: MessagesState) -> dict:
    """LLM decides whether to call a tool or respond."""
    messages = [
        SystemMessage(content="You are a helpful math assistant. Use tools for calculations."),
        *state["messages"]
    ]
    
    result = model_with_tools.invoke(messages)  # ✅ Uses imported model_with_tools
    return {
        "messages": [result],
        "llm_calls": state.get('llm_calls', 0) + 1
    }

def tool_node(state: MessagesState) -> dict:
    """Execute tool calls and return results."""
    last_message = state["messages"][-1]
    result = []
    
    for tool_call in last_message.tool_calls:
        tool = tools_by_name[tool_call["name"]]  # ✅ Uses imported tools_by_name
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(
            content=str(observation), 
            tool_call_id=tool_call["id"]
        ))
    
    return {"messages": result}