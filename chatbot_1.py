## A simple chat bot ##

import subprocess

def ask_ollama(prompt):
    # Run ollama CLI with subprocess
    result = subprocess.run(
        ["ollama", "run", "qwen3:4b"],
        input=prompt.encode("utf-8"),
        capture_output=True
    )
    return result.stdout.decode("utf-8")

# First test
user_message = "Hello how are you?"
response = ask_ollama(user_message)

print("User:", user_message)
print("Bot:", response.strip())