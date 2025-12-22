"""Email Responder Agent - Full LangGraph workflow."""
from typing import Literal
from langgraph.graph import StateGraph, START, END
from .utils.state import AgentState
from .utils.node import classify_email, load_response_template, generate_reply, human_review



# BUILD GRAPH
builder = StateGraph(AgentState)

# ADD NODES
builder.add_node("classify", classify_email)
builder.add_node("template", load_response_template)
builder.add_node("generate", generate_reply)
builder.add_node("review", human_review)

# ADD EDGES
builder.add_edge(START, "classify")
builder.add_edge("classify", "template")
builder.add_edge("template", "generate")
builder.add_edge("generate", "review")
builder.add_edge("review", END)

# COMPILE
graph = builder.compile()


def run_agent():
    """Interactive CLI demo."""
    print("📧 Email Responder Agent (Qwen3)")
    print("=" * 50)
    
    while True:
        email = input("\nEmail> ").strip()
        if email.lower() in ["exit", "quit"]:
            break
            
        # Run full graph
        result = graph.invoke({
            "email": email,
            "category": "",
            "template": "",
            "draft": "",
            "approved": False,
            "customer_name": ""
        })
        
        print(f"\n🎉 Final status: {'✅ SENT' if result['approved'] else '❌ NEEDS WORK'}")
        print("-" * 50)


if __name__ == "__main__":
    run_agent()
