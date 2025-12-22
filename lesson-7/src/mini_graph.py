"""Main LangGraph app - nodes, edges, state, flow control demo."""
from typing import Literal

from langgraph.graph import StateGraph, START, END
from .nodes.core_nodes import GraphState, classify_question, answer_from_docs, ask_clarification


# BUILD GRAPH
builder = StateGraph(GraphState)

# 1️⃣ ADD NODES
builder.add_node("classify", classify_question)
builder.add_node("docs", answer_from_docs)
builder.add_node("clarify", ask_clarification)

# 2️⃣ ADD EDGES (flow control)
builder.add_edge(START, "classify")

def route_decision(state: GraphState) -> Literal["docs", "clarify"]:
    """Conditional edge: decide next node based on state."""
    print(f"🔀 [route] category='{state['category']}'")
    return "docs" if state["category"] != "other" else "clarify"

builder.add_conditional_edges(
    "classify",
    route_decision,
    {"docs": "docs", "clarify": "clarify"}
)

# Terminal edges
builder.add_edge("docs", END)
builder.add_edge("clarify", END)

# 3️⃣ COMPILE (this is the graph object)
graph = builder.compile()


# CLI RUNNER
def run_demo():
    """Interactive demo to see graph execution."""
    print("🚀 LangGraph Fundamentals Demo")
    print("Try: 'explain langgraph', 'python code help', 'hello'")
    print("-" * 50)
    
    while True:
        question = input("\nQ> ").strip()
        if question.lower() in ["exit", "quit"]:
            break
            
        # Run graph
        result = graph.invoke({
            "question": question,
            "category": "",
            "answer": ""
        })
        
        print(f"\n✅ Answer: {result['answer']}")
        print(f"📊 Final state: {result}")


if __name__ == "__main__":
    run_demo()
