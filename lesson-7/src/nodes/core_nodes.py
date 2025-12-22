from typing_extensions import TypedDict


class GraphState(TypedDict):
    """Shared state passed between all nodes."""
    question: str
    category: str
    answer: str


def classify_question(state: GraphState) -> dict:
    """Node 1: Classify the question type."""
    q = state["question"].lower()
    
    if any(word in q for word in ["code", "python", "js", "javascript"]):
        category = "code"
    elif any(word in q for word in ["what is", "explain", "why", "how"]):
        category = "explain"
    else:
        category = "other"
    
    print(f"🔍 [classify] '{state['question'][:30]}...' → category='{category}'")
    return {"category": category}


def answer_from_docs(state: GraphState) -> dict:
    """Node 2: Generate answer from 'docs' (static for now)."""
    if state["category"] == "code":
        ans = "Here's your code solution from the docs..."
    else:
        ans = "Here's the explanation from the docs..."
    
    print(f"📚 [docs] Generated answer for '{state['category']}'")
    return {"answer": ans}


def ask_clarification(state: GraphState) -> dict:
    """Node 3: Ask user to clarify."""
    ans = "Sorry, I don't understand. Can you rephrase?"
    print("❓ [clarify] Needs more info")
    return {"answer": ans}
