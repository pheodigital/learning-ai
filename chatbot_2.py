## A simple chat bot with interactive mode ##

import subprocess

#ask_ollama function
def ask_ollama(user_input):
  # Add instructions for clean reply
  prompt = f""" You are a chatbot. Reply ONLY in final plain text. Do NOT include reasoning, explanations, or any extra text.User said: "{user_input}" Reply in plain text: """
  
  #Run ollama CLT with subprocess
  result = subprocess.run(
    ["ollama", "run", "qwen3:4b"],
    input=prompt.encode("utf-8"),
    capture_output=True,
  )
  # Decode from bytes → string and return
  return result.stdout.decode("utf-8").strip()

def chat():
  print("Chatbot ready! Type 'exit' to quit.\n")
  while True:
    #Get user input
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "bye", "q"]:
      print("Bot: Says good bye")
      break

    #Ask model
    response = ask_ollama(user_input)
    print("Bot:", response)


# Run chatbot
# “Only run this part if the file is executed directly, not when imported into another file.”
if __name__ == "__main__":
    chat()