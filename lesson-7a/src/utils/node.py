from typing import Literal
import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from .state import AgentState
from .templates import load_templates, extract_customer_name


load_dotenv()
model_name = os.getenv("OLLAMA_MODEL", "qwen3:4b")


def classify_email(state: AgentState) -> AgentState:
    """Classify email into categories."""
    email = state["email"].lower()
    
    if any(word in email for word in ["urgent", "asap", "emergency", "failed 3"]):
        category = "urgent"
    elif any(word in email for word in ["error", "bug", "broken", "python", "code"]):
        category = "technical"
    elif any(word in email for word in ["payment", "billing", "refund", "charge"]):
        category = "billing"
    else:
        category = "general"
    
    print(f"🔍 [classify] '{state['email'][:50]}...' → {category}")
    return {"category": category}


def load_response_template(state: AgentState) -> AgentState:
    """Load category-specific template."""
    template = load_templates(state["category"])
    name = extract_customer_name(state["email"])
    
    print(f"📄 [template] Loaded {state['category']} template for {name}")
    return {
        "template": template or "Default response template",
        "customer_name": name
    }


def generate_reply(state: AgentState) -> AgentState:
    """Use Qwen3 to generate personalized reply."""
    llm = ChatOllama(model=model_name, temperature=0.1)
    
    prompt = f"""
    Email: {state['email']}
    Template: {state['template']}
    Customer: {state['customer_name']}
    
    Generate a professional, personalized reply using the template.
    Keep it under 150 words.
    """
    
    response = llm.invoke(prompt)
    draft = response.content.format(customer_name=state['customer_name'])
    
    print(f"🤖 [Qwen3] Generated draft ({len(draft)} chars)")
    return {"draft": draft}


def human_review(state: AgentState) -> AgentState:
    """Human-in-the-loop approval."""
    print(f"\n📧 DRAFT:\n{state['draft']}\n")
    print("Commands: approve | edit | reject")
    
    while True:
        decision = input("Your decision> ").strip().lower()
        
        if decision == "approve":
            print("✅ APPROVED - Email sent!")
            return {"approved": True}
        elif decision == "edit":
            edit = input("Your edit> ")
            return {"draft": state['draft'] + f"\n\nEDIT: {edit}", "approved": False}
        elif decision == "reject":
            print("❌ REJECTED - Restarting...")
            return {"approved": False}
        else:
            print("Type: approve/edit/reject")
