# Email Responder Agent - LangGraph Project

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.0%2B-orange)](https://langchain-ai.github.io/langgraph/)
[![Ollama](https://img.shields.io/badge/Ollama-qwen3:4b-green)](https://ollama.ai/)

**Real-world customer support agent** that classifies emails (urgent/technical/billing/general), loads templates, generates personalized replies with Qwen3, and supports human approval.

## 🎯 **What it does**

Customer Email → classify type → load template → Qwen3 generates reply → human approve → send

**Demo flow:**

"Payment failed, urgent!" → urgent → "We're fixing this ASAP..." → APPROVE → "Sent!"

## 📁 **Folder Structure**

email-responder/
├── .venv/ # Virtual environment
├── requirements.txt # pip install -r requirements.txt
├── .env # OLLAMA_MODEL=qwen3:4b
├── README.md # This file
├── langgraph.json # Graph manifest
└── src/
├── init.py
├── agent.py # Main graph + CLI
├── templates/ # Response templates
│ ├── urgent.txt
│ ├── technical.txt
│ └── billing.txt
└── utils/
├── state.py # AgentState TypedDict
├── nodes.py # classify/generate/approve nodes
└── templates.py # Template loader

## 🚀 **Quick Start (macOS)**

### 1. Setup

```bash
git clone <this-repo> email-responder
cd email-responder

# Create & activate venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

2. Configure Ollama

# Ensure your models are ready
ollama list  # Should show qwen3:4b
ollama pull qwen3:4b  # If missing

3. Edit .env

# Add your model
echo "OLLAMA_MODEL=qwen3:4b" >> .env

4. Run

python -m src.agent

5. Test it

Email> "My payment failed 3 times! Urgent help!"
🔍 [classify] → "urgent"
📄 [template] → "We're fixing payments ASAP..."
🤖 [Qwen3] → "Hi John, sorry for the payment issue. We've..."
✅ [approve] → Type: approve/edit/reject

```

🏗️ Architecture

[START]
↓ (input: email text)
[classify_email] ──→ "urgent|technical|billing|general"
↓ (conditional edge)
[load_template] ──→ category-specific template
↓
[generate_reply] ──→ Qwen3(template + email) → personalized draft
↓
[human_review] ───→ APPROVE | EDIT | REJECT (END)

State evolution:

# Initial

{"email": "Payment failed!", "category": "", "draft": ""}

# After classify

{"email": "...", "category": "urgent", "draft": ""}

# After generate

{"email": "...", "category": "urgent", "draft": "Hi John, we've fixed..."}

🔧 Files Explained

| File                   | Purpose                                        |
| ---------------------- | ---------------------------------------------- |
| src/agent.py           | Wires nodes/edges, compiles graph, runs CLI    |
| src/utils/state.py     | AgentState TypedDict (shared memory)           |
| src/utils/nodes.py     | 4 nodes: classify, template, LLM, human-review |
| src/utils/templates.py | Loads .txt templates by category               |
| src/templates/\*.txt   | Pre-written response templates                 |
| langgraph.json         | Declares email_router graph for tooling        |

CLI Commands

Email> "Login broken after update"
→ classifies "technical" → loads tech template → Qwen3 reply → [approve/edit/reject]

Commands at human review:

- approve → Finalize & "send"
- edit → Modify draft → regenerate
- reject → Restart from beginning
- exit → Quit app

Example Inputs/Outputs

| Input Email           | Category  | Final Reply                               |
| --------------------- | --------- | ----------------------------------------- |
| "Payment failed 3x!"  | urgent    | "Hi, payment team is on it NOW..."        |
| "Python error in API" | technical | "Here's the fix for your Python issue..." |
| "Where's my refund?"  | billing   | "Your refund processed on DATE..."        |

Next Level (Extend this)
Add more templates → src/templates/sales.txt

Real email integration → Gmail/IMAP node

Multiple LLMs → Switch between Qwen3/Nomic

Vector store → RAG over support docs

Deploy → FastAPI + LangGraph Cloud

Troubleshooting

| Issue               | Fix                                                          |
| ------------------- | ------------------------------------------------------------ |
| ModuleNotFoundError | source .venv/bin/activate && pip install -r requirements.txt |
| Ollama not found    | ollama serve & (background)                                  |
| qwen3:4b missing    | ollama pull qwen3:4b                                         |
| Import errors       | Ensure all **init**.py files exist                           |

📚 LangGraph Concepts Demonstrated
✅ State: AgentState TypedDict flows through nodes

✅ Nodes: Pure functions (state → partial state)

✅ Edges: Fixed + conditional routing

✅ Flow Control: Classify → template → LLM → human loop

✅ LLM Integration: Qwen3 inside generate_reply node

✅ Human-in-loop: Interrupt + resume pattern

Built for learning LangGraph fundamentals with real-world applicability. Scale to production by swapping templates/LLMs! 🚀

Author: AI Mentor | Date: Dec 2025

**To save as `README.md`:**

1. Copy the entire code block above
2. Create `README.md` in your `email-responder/` folder
3. Paste and save
4. Done! 🎉

The file is complete with badges, tables, code blocks, and perfect GitHub rendering. Ready for your project!
