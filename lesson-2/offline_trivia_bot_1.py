## A simple trivia ##

import subprocess
import time

# loader function
def loading_indicator():
  print("\n")
  print("Bot is thinking:")
  print("\n")
  print(f"Loading...")
  print("\n")
  for i in range(0, 101, 20): #increment of 20%
    time.sleep(0.3)


def ask_ollama(category, question):
  """Ask the local Ollama model (no internet needed)."""

  # System prompt: behave as a trivia expert #
  prompt = f"You are a trivia expert. Answer this {category} question clearly and briefly:\n\n{question}"
  
  loading_indicator()  # show loading first
  #Run ollama CLT with subprocess
  result = subprocess.run(
    ["ollama", "run", "qwen3:4b"],
    input=prompt.encode("utf-8"),
    capture_output=True,
  )

  output = result.stdout.decode("utf-8").strip()

  # ✅ Keep only the text after "...done thinking."
  if "...done thinking." in output:
    output = output.split("...done thinking.", 1)[1].strip()

# Decode from bytes → string and return
  return output


def trivia_chat():
  print("\n")
  print("Welcome to the Trivia Chatbot!")
  print("\n")
  print("Categories: Science, History, Sports")
  print("\n")
  print("Offline Trivia AI ready! Type 'exit' to quit.")
  print("\n")

  while True:
    category = input("Choose a category: ").strip().lower()
    print("\n")

    if category in ["exit", "quit", "q"]:
        print("Bot: Goodbye! 👋")
        print("\n")
        break

    if category not in ["science", "history", "sports"]:
        print("Bot: Please choose a valid category (Science, History, Sports).")
        print("\n")
        continue

    question = input(f"Ask a {category.capitalize()} question: ")

    if question.lower() in ["exit", "quit", "q"]:
        print("Bot: Goodbye! 👋")
        print("\n")
        break

    response = ask_ollama(category, question)
    print(f"Bot: ({category.capitalize()}): {response}\n")

# Run chatbot
# “Only run this part if the file is executed directly, not when imported into another file.”
if __name__ == "__main__":
  trivia_chat()