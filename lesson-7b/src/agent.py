"""LangGraph Math Agent - Official Quickstart."""
from typing import Literal
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
from .utils.state import MessagesState
from .utils.nodes import llm_call, tool_node

def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Route to tools or end based on tool calls."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool_node"
    return END

# BUILD GRAPH
builder = StateGraph(MessagesState)
builder.add_node("llm_call", llm_call)
builder.add_node("tool_node", tool_node)

# EDGES
builder.add_edge(START, "llm_call")
builder.add_conditional_edges(
    "llm_call", 
    should_continue, 
    {"tool_node": "tool_node", END: END}
)
builder.add_edge("tool_node", "llm_call")

# COMPILE
graph = builder.compile()

def run_demo():
    """Interactive math agent demo."""
    print("🧮 Math Agent (Claude + Tools)")
    print("=" * 40)
    
    while True:
        query = input("\nMath> ").strip()
        if query.lower() in ["exit", "quit"]:
            break
            
        # Run agent
        result = graph.invoke({
            "messages": [HumanMessage(content=query)],
            "llm_calls": 0
        })
        
        print("\n📊 Final Messages:")
        for msg in result["messages"]:
            msg_type = msg.__class__.__name__
            content = msg.content or "TOOL CALL"
            print(f"[{msg_type}] {content}")
        print(f"LLM calls: {result['llm_calls']}\n")

if __name__ == "__main__":
    run_demo()
