#!/usr/bin/env python3
"""
Step-by-step Calculator (Gradio UI)
Uses Ollama + LangChain to show reasoning steps for math expressions,
and verifies the final numeric answer using a safe local evaluator.
"""

import gradio as gr
import re
import ast
import operator
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

# ---------- Safe arithmetic evaluator ----------
ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: lambda x: x,
    ast.USub: operator.neg,
}

def safe_eval(expr: str):
    expr = expr.replace(",", "")
    node = ast.parse(expr, mode='eval')

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numeric constants allowed")
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in ALLOWED_OPERATORS:
                raise ValueError(f"Disallowed operator: {op_type}")
            left = _eval(node.left)
            right = _eval(node.right)
            return ALLOWED_OPERATORS[op_type](left, right)
        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in ALLOWED_OPERATORS:
                raise ValueError(f"Disallowed unary operator: {op_type}")
            operand = _eval(node.operand)
            return ALLOWED_OPERATORS[op_type](operand)
        raise ValueError(f"Unsupported expression: {type(node).__name__}")

    return _eval(node)

# ---------- LLM setup ----------
llm = ChatOllama(model="qwen3:4b")

template = """
You are a calm math tutor.
Solve the arithmetic expression step-by-step.
If mode is 'show_steps', display your reasoning with numbered steps.
If mode is 'final_only', only show the numeric result.

Expression: {expression}
Mode: {mode}

Format your final answer as:
Final Answer: <number>
"""

prompt = PromptTemplate(
    input_variables=["expression", "mode"],
    template=template
)

def extract_final_numeric(text: str):
    match = re.search(r"Final Answer\s*[:\-]\s*([+-]?\d+(?:\.\d+)?)", text, re.IGNORECASE)
    if match:
        s = match.group(1)
        return float(s) if '.' in s else int(s)
    nums = re.findall(r"[+-]?\d+(?:\.\d+)?", text)
    if nums:
        last = nums[-1]
        return float(last) if '.' in last else int(last)
    return None

# ---------- Main logic ----------
def solve_expression(expression, show_steps):
    if not expression.strip():
        return "Please enter an expression.", ""

    mode = "show_steps" if show_steps else "final_only"
    formatted = prompt.format(expression=expression, mode=mode)
    model_output = llm.invoke(formatted)

    parsed = extract_final_numeric(str(model_output))
    try:
        computed = safe_eval(expression)
        match = (parsed is not None) and abs(float(parsed) - float(computed)) < 1e-9
        verified_text = f"✅ Verified: {computed}" if match else f"❌ Mismatch (Computed: {computed}, Model: {parsed})"
    except Exception as e:
        verified_text = f"⚠️ Could not verify: {e}"

    return str(model_output), verified_text

# ---------- Gradio UI ----------
iface = gr.Interface(
    fn=solve_expression,
    inputs=gr.Textbox(label="Enter your math problem", placeholder="e.g. 12 + (6 × 2) - 4"),
    outputs=[
        gr.Textbox(label="Model Reasoning", lines=12, max_lines=25, elem_id="reasoning_box", interactive=False),
        gr.Textbox(label="Final Answer", lines=2, max_lines=4, elem_id="answer_box", interactive=False)
    ],
    title="🧮 Step-by-Step AI Calculator",
    css="""
        #reasoning_box {
            background-color: #f5f5f5;
            font-family: 'Courier New', monospace;
            color: #333;
            border-radius: 10px;
            border: 1px solid #ddd;
        }
        #answer_box {
            background-color: #e8ffe8;
            font-weight: bold;
            color: #111;
            border-radius: 8px;
            border: 1px solid #aaaa;
        }
    """
)

if __name__ == "__main__":
    iface.launch()
