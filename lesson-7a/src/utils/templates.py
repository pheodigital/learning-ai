import os
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

def load_templates(category: str) -> Optional[str]:
  """Load template by category."""
  template_path = f"src/templates/{category}.txt"

  if(os.path.exists(template_path)):
    with open(template_path, 'r') as file:
      return file.read()

  return None

def extract_customer_name(email: str) -> str:
  """Simple name extraction (production: use NER)."""
  lines = email.split("\n")

  for line in lines:
    if "name" in line.lower() or "@" in line:
      return line.split("@")[0].replace("Hi, ", "").capitalize()
  return "Customer"


