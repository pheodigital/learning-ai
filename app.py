#!/usr/bin/env python3
"""
step_calc.py

Step-by-step calculator using Ollama (local LLM) + LangChain helper
Includes a safe arithmetic evaluator to verify model answers.
"""
## This is the langchain_ollama package. ##
from langchain_ollama import ChatOllama
## langchain-core defines the base abstractions for the LangChain ecosystem. ##
from langchain_core.prompts import PromptTemplate
## Support for regular expressions (RE). ##
import re
## The `ast` module helps Python applications to process trees of the Python abstract syntax grammar. ##
import ast
## Operator Interface ## 
import operator

# ---------- Safe arithmetic evaluator ----------
# Accepts arithmetic expressions and evaluates them with AST for safety.
# Supports: + - * / // % ** parentheses, unary +/-
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
    """
    Safely evaluate arithmetic expression expr.
    Raises ValueError if expression contains disallowed nodes.
    """
    # normalize: remove commas in numbers like "1,234" -> "1234" (optional)
    expr = expr.replace(",", "")
    node = ast.parse(expr, mode='eval')

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):  # Python 3.8+: numbers appear as Constant
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numeric constants allowed")
        if isinstance(node, ast.Num):  # older AST node
            return node.n
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
        if isinstance(node, ast.Call):
            raise ValueError("Function calls are not allowed")
        raise ValueError(f"Unsupported expression: {type(node).__name__}")

    return _eval(node)

# ---------- LLM + prompt ----------
# Use your local Ollama chat model (change model name if needed)
llm = ChatOllama(model="qwen3:4b")  # or ChatOllama(model="qwen3:4b") etc.

# Prompt template: instruct the model how to format steps and final answer
step_template_text = """
You are a patient math tutor. The user gives a single arithmetic expression to solve.
When asked to show steps, do the following:
1) Provide a clear numbered step-by-step explanation of how to compute the expression.
2) At the end, clearly write: Final Answer: <number>

If asked NOT to show steps, only output the final numeric answer (no extra text).

Do not include chain-of-thought or internal reasoning beyond numbered steps.
Keep steps short and precise.

Expression: "{expression}"
Mode: "{mode}"   # mode is either "show_steps" or "final_only"
"""

prompt = PromptTemplate(input_variables=["expression", "mode"], template=step_template_text)

def ask_model(expression: str, show_steps: bool = True) -> str:
    """
    Format prompt and call the model; returns raw model text.
    """
    mode = "show_steps" if show_steps else "final_only"
    formatted = prompt.format(expression=expression, mode=mode)
    # For ChatOllama, use invoke to get text
    resp = llm.invoke(formatted)
    # Some wrappers return strings directly; ensure string
    return str(resp).strip()

# ---------- Helpers to extract numeric answer from model output ----------
def extract_final_numeric(text: str):
    """
    Attempt to find the final numeric answer in model text.
    Looks for lines like 'Final Answer: 42' or any number-like token at the end.
    Returns the numeric value (int/float) or None.
    """
    # 1) Look for 'Final Answer:' pattern
    m = re.search(r"Final Answer\s*[:\-]\s*([+-]?\d+(?:\.\d+)?)", text, re.IGNORECASE)
    if m:
        s = m.group(1)
        return float(s) if '.' in s else int(s)
    # 2) Fallback: search for last numeric token in text
    nums = re.findall(r"[+-]?\d+(?:\.\d+)?", text)
    if nums:
        last = nums[-1]
        return float(last) if '.' in last else int(last)
    return None

# ---------- Main interactive function ----------
def solve_expression_interactive(expression: str, show_steps: bool = True):
    print("User expression:", expression)
    model_text = ask_model(expression, show_steps=show_steps)
    print("\n--- Model output ---")
    print(model_text)
    print("--------------------\n")

    parsed_answer = extract_final_numeric(model_text)
    verified = None
    verification_message = ""
    try:
        computed = safe_eval(expression)
        verified = True if (parsed_answer is not None and abs(float(parsed_answer) - float(computed)) < 1e-9) else False
        verification_message = f"Computed locally: {computed}"
    except Exception as e:
        computed = None
        verification_message = f"Local evaluation error: {e}"
        verified = False

    print("Parsed model numeric answer:", parsed_answer)
    print(verification_message)
    if computed is not None:
        if verified:
            print("✅ Model answer matches local computation.")
        else:
            print("❌ MISMATCH: Model answer does not match local computation.")
            if parsed_answer is None:
                print("Note: could not parse numeric answer from model output.")
            else:
                print(f"Model parsed: {parsed_answer} vs computed: {computed}")

    return {
        "expression": expression,
        "model_text": model_text,
        "parsed_answer": parsed_answer,
        "computed": computed,
        "verified": verified,
    }

# ---------- Example usage ----------
if __name__ == "__main__":
    # Try with steps
    solve_expression_interactive("12 * (3 + 4)", show_steps=True)

    # Try final only
    solve_expression_interactive("2.5 * (4 + 6) - 3", show_steps=False)
