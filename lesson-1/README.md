## Simple Python Chatbot Using Ollama (qwen3:4b)

This project demonstrates how to build a simple command-line chatbot using the ollama CLI with the qwen3:4b language model. It includes:

Basic non-interactive prompt-response

Interactive chatbot loop

Loading indicator for better UX

Requirements

Before running the code, ensure you have the following installed:

      Python 3.7+

      Ollama
      CLI installed and configured

The qwen3:4b model pulled using:

ollama pull qwen3:4b

# Files Overview

      There are three main versions of the chatbot code:

      1. ✅ Non-interactive Version
         user_message = "Hello how are you?"
         response = ask_ollama(user_message)
         print("User:", user_message)
         print("Bot:", response.strip())

      Sends a single message to the model and prints the result.

      2. 💬 Interactive Chat Version
         def chat():
         while True:
         user_input = input("You: ")
         if user_input.lower() in ["exit", "quit", "bye"]:
         break
         response = ask_ollama(user_input)
         print("Bot:", response.strip())

      Allows for ongoing conversation until the user types "exit", "quit", or "bye".

      3. ⏳ Interactive Chat + Loading Indicator
         def loading_indicator():
         for i in range(0, 101, 20):
         time.sleep(0.3)

      Simulates the model "thinking" before generating a response, enhancing user experience.

# Key Concepts and Keywords

      Keyword / Method Description
      subprocess.run() Executes the ollama CLI command to run the model. It sends input and captures output.
      ["ollama", "run", "qwen3:4b"] Runs the model named qwen3:4b using the ollama CLI.
      .encode("utf-8") Converts the prompt (string) to bytes so it can be sent to the subprocess.
      .decode("utf-8") Converts the model's byte output back into a readable string.
      if **name** == "**main**": Ensures the chat() function runs only when the script is executed directly (not when imported).
      input() Collects input from the user in the terminal.
      .strip() Cleans leading/trailing whitespace from the model’s response.

      🚀 How to Run

      Save your Python script, e.g., chatbot.py

      Run from terminal:

      python chatbot.py

      Start chatting:

      You: Hello
      Bot: Hi there! How can I help you today?

      To exit:

      You: exit
      Bot: Goodbye 👋

      💡 Notes

      You can replace "qwen3:4b" with any other model you've pulled using Ollama (e.g., "llama2:7b", "mistral", etc.)

      Use strip() on responses to remove trailing whitespace or newlines.

      Add exception handling for production use (e.g., try-except around subprocess).

# Example Output

      Chatbot ready! Type 'exit' to quit.

      You: What's the weather like today?
      Bot: I'm a language model and don't have real-time data, but you can check a weather app!
