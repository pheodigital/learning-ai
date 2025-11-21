## A simple chat bot with interactive mode  and loding ##

import subprocess
import time

def loading_indicator():
  print("Bot is thinking:")
  print(f"Loading...")
  print()  # new line
  for i in range(0, 101, 20): #increment of 20%
    time.sleep(0.3)


def clean_bot_response(response):
    # Remove known 'thinking' lines or reasoning markers
    reasoning_lines = [
        "Hmm, the user just",  # Common Qwen reasoning lead
        "I need to respond", 
        "Since they're greeting me", 
        "No need to add anything else",
        "Just the phrase", 
        "#", 
        "checks requirements again",
        "...done thinking."
    ]
    lines = response.splitlines()
    filtered = [
        line for line in lines
        if not any(r in line for r in reasoning_lines)
        and not line.strip().startswith("*")  # remove actions
    ]
    # Remove empty lines
    filtered = [line for line in filtered if line.strip() != ""]
    return "\n".join(filtered).strip()


#ask_ollama function
def ask_ollama(conversation_history):
  """
  conversation_history: list of tuples (role, message)
  role: "user" or "bot"
  """
  # Build the prompt with history
  prompt_text = "You are a helpful chatbot. Reply ONLY in final plain text. Do NOT include reasoning.\n\n"

  for role, message in conversation_history:
    if role == "user":
      prompt_text += f"User: {message}\n"
    elif role == "bot":
      prompt_text += f"Bot: {message}\n"
  prompt_text += "Bot:"
    
  
  loading_indicator()  # show loading first
  
  #Run ollama CLT with subprocess
  result = subprocess.run(
    ["ollama", "run", "qwen3:4b"],
    input=prompt_text.encode("utf-8"),
    capture_output=True,
  )
  
  # Decode and strip possible prefix
  response = result.stdout.decode("utf-8").strip()
  
  # Remove possible "Bot:" at the beginning, if present
  if response.startswith("Bot:"):
      response = response[len("Bot:"):].strip()
  
  response = clean_bot_response(response)   
  return response


def chat():
  print("🤖 Chatbot ready! Type 'exit' 'quit' 'q' to quit.\n")
  conversation_history = []

  while True:
    #Get user input
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "bye", "q"]:
      print("Bot: Says good bye")
      break
    
    # Add user message to history
    conversation_history.append(("user", user_input))

    # Get bot response
    response = ask_ollama(conversation_history)

    # Print response and add to history
    print("Bot:", response)
    conversation_history.append(("bot", response))


# Run chatbot
# “Only run this part if the file is executed directly, not when imported into another file.”
if __name__ == "__main__":
    chat()