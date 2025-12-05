import streamlit as st

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_classic.chains import RetrievalQA

# ----- CONFIG -----
CHAT_MODEL = "qwen3:4b"          # any chat-capable model you have in Ollama
EMBED_MODEL = "nomic-embed-text" # any embedding model you have in Ollama
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
PERSIST_DIR = "chroma_notes_db"  # folder for local vector store


# ----- HELPERS -----
@st.cache_resource
def get_llm():
    return ChatOllama(model=CHAT_MODEL, temperature=0.1)


@st.cache_resource
def get_embeddings():
    return OllamaEmbeddings(model=EMBED_MODEL)


# ----- load_documents -----
def load_documents(uploaded_file):
  if uploaded_file.name.lower().endswith(".pdf"):
    # Save uploaded file to a temp location so PyPDFLoader can read it
    temp_path = f"temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
      f.write(uploaded_file.getbuffer())
    loader = PyPDFLoader(temp_path)
    docs = loader.load()
  else:
    # Treat as plain text / markdown
    text = uploaded_file.read().decode("utf-8", errors="ignore")
    docs = [Document(page_content=text)]
  return docs


# ----- create/update vector store -----
def create_or_update_vectorstore(docs, embeddings):
  splitter = RecursiveCharacterTextSplitter(
      chunk_size=CHUNK_SIZE,
      chunk_overlap=CHUNK_OVERLAP,
  )
  chunks = splitter.split_documents(docs)

  # Simple approach: recreate vector store each time new file is uploaded
  vectordb = Chroma.from_documents(
      documents=chunks,
      embedding=embeddings,
      persist_directory=PERSIST_DIR,
  )
  vectordb.persist()
  return vectordb

# ----- get qa chain -----
def get_qa_chain(vectordb, llm):
  retriever = vectordb.as_retriever(search_kwargs={"k": 4})
  qa_chain = RetrievalQA.from_chain_type(
      llm=llm,
      retriever=retriever,
      chain_type="stuff",  # simple: put retrieved chunks into the prompt
  )
  return qa_chain


# ----- STREAMLIT APP -----
def main():
  st.set_page_config(page_title="Mini RAG Notes Chat", page_icon="📚")
  st.title("📚 Mini RAG – Chat with Your Notes")

  st.sidebar.header("Upload notes")
  uploaded_file = st.sidebar.file_uploader(
      "Upload a note (PDF / TXT / MD)", type=["pdf", "txt", "md"]
  )

  if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
  
  if uploaded_file is not None and st.sidebar.button("Build knowledge base"):
    with st.spinner("Reading & indexing your note..."):
      docs = load_documents(uploaded_file)
      embeddings = get_embeddings()
      vectordb = create_or_update_vectorstore(docs, embeddings)
      llm = get_llm()
      st.session_state.qa_chain = get_qa_chain(vectordb, llm)
    st.sidebar.success("Knowledge base ready! Ask questions below ⬇️")

  st.write("1. Upload a file in the sidebar.\n2. Click **Build knowledge base**.\n3. Ask questions in the chat box.")

  if st.session_state.qa_chain is None:
    st.info("Upload a note and build the knowledge base to start chatting.")
    return

  # Simple chat UI
  if "messages" not in st.session_state:
      st.session_state.messages = []

  for msg in st.session_state.messages:
      with st.chat_message(msg["role"]):
          st.markdown(msg["content"])

  user_input = st.chat_input("Ask something about your note...")
  if user_input:
      st.session_state.messages.append({"role": "user", "content": user_input})
      with st.chat_message("user"):
          st.markdown(user_input)

      with st.chat_message("assistant"):
          with st.spinner("Thinking..."):
              answer = st.session_state.qa_chain.run(user_input)
              st.markdown(answer)
      st.session_state.messages.append({"role": "assistant", "content": answer})


# ----- MAIN -----
if __name__ == "__main__":
  main()