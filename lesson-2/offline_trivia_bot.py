## A simple trivia ##

import subprocess
import time

# loader function
def loading_indicator():
  print("Bot is thinking:")
  print(f"Loading...")
  print()  # new line
  for i in range(0, 101, 20): #increment of 20%
    time.sleep(0.3)


def ask_ollama(prompt):
  """Ask the local Ollama model (no internet needed)."""

  # System prompt: behave as a trivia expert #
  system_instruction = """ You are a trivia expert.  Answer questions briefly and accurately in plain text. Do NOT include reasoning or thought process. """

  # Combine system prompt + user input #
  full_prompt = system_instruction + f"\n Question: {prompt} \nAnswer:"
  
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

  return output


  # Decode from bytes → string and return
  return result.stdout.decode("utf-8").strip()


def trivia_chat():
  print(" Offline Trivia AI ready! Type 'exit' to quit. \n")

  while True:
    user_input = input("Ask a trivia question: ")

    if user_input.lower() in ["exit", "quit", "bye", "q"]:
      print("Bot: Says good bye")
      break

    response = ask_ollama(user_input)
    print("Bot:", response, "\n")

# Run chatbot
# “Only run this part if the file is executed directly, not when imported into another file.”
if __name__ == "__main__":
  trivia_chat()