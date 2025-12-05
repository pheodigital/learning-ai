# Mini RAG Notes Chat App

This is a beginner-friendly mini Retrieval-Augmented Generation (RAG) app built with Streamlit, LangChain, Ollama, and Chroma vector store. It lets you upload notes (PDF/TXT/MD), build a local knowledge base with embeddings, and chat interactively with your documents using local Ollama LLMs.

---

## Features

- Upload PDF, text, or markdown notes
- Split text into manageable chunks for embedding
- Use Ollama local models for embeddings and chat completions
- Store embeddings locally using Chroma vector database
- Simple interactive chat UI with Streamlit

---

## Tech Stack

| Component                | Description                                              |
| ------------------------ | -------------------------------------------------------- |
| Python 3.11+             | Runtime environment                                      |
| Streamlit                | Web UI framework                                         |
| Ollama                   | Local LLM and embedding models                           |
| LangChain-core           | Core LangChain functionality                             |
| LangChain-text-splitters | Text chunking utilities                                  |
| LangChain-community      | Document loaders (PDF) and vectorstore wrappers (Chroma) |
| LangChain-classic        | Legacy chains like RetrievalQA                           |
| Chroma                   | Local vector database                                    |
| pypdf                    | PDF text extraction                                      |

---

## Setup Instructions

1. **Clone the repository (or copy the code).**

2. **Create and activate a Python virtual environment:**

python3 -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows

3. **Create `requirements.txt` with the following:**

langchain-core
langchain-text-splitters
langchain-community
langchain-ollama
langchain-classic
chromadb
pypdf
streamlit

4. **Install dependencies:**

pip install -r requirements.txt --upgrade

5. **Make sure Ollama server is running and you have pulled models:**

ollama pull qwen3:4b
ollama pull nomic-embed-text

---

## Running the App

Run the Streamlit app with:

streamlit run app.py

In your browser:

- Upload a note file in the sidebar (PDF, TXT, or Markdown).
- Click **Build knowledge base** to process your note.
- Start chatting with your uploaded notes in the chat interface.

---

## How it works

- Uploaded notes are loaded and split into smaller chunks.
- Each chunk is converted into embeddings using Ollama’s embedding model.
- Embeddings are stored locally in a Chroma vector store.
- When you ask questions, the app retrieves relevant chunks and generates answers using the Ollama chat LLM.

---

## Notes

- This app uses the latest LangChain v1.0+ modular package architecture as of Dec 2025.
- Legacy chains like `RetrievalQA` are imported from `langchain_classic`.
- Text splitters are imported from the separate `langchain-text-splitters` package.
- Document loaders and vector DB wrappers are from `langchain-community`.
- You need to have Ollama installed and running locally with the correct models pulled.

---

## License

This project is provided for educational and prototyping purposes. Feel free to modify and share!

---

## References

- [LangChain v1 Migration Guide](https://docs.langchain.com/oss/python/migrate/langchain-v1)
- [Ollama Python documentation](https://github.com/ollama/ollama-python)
- [Streamlit documentation](https://docs.streamlit.io/)
- [Chroma vector database](https://chroma.tech/)

This README covers the app usage, setup, architecture, and dependencies clearly for a beginner starting from the code provided. It ensures the newest LangChain modular packages are mentioned correctly with citations to official docs
