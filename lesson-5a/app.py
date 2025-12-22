import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA  # Correct top-level import currently supported


st.set_page_config(page_title="Ask Your PDF", layout="wide")
st.title("📄 Ask Your PDF (Ollama + Chroma)")


# ------------------------------
# Upload PDFs
uploaded_files = st.file_uploader(
    "Upload one or more PDFs",
    type="pdf",
    accept_multiple_files=True
)


if uploaded_files:
    st.info("Loading PDFs and preparing vector store... This may take a few seconds.")

    # Load all PDFs
    all_documents = []
    for file in uploaded_files:
        loader = PyPDFLoader(file)
        docs = loader.load()
        all_documents.extend(docs)

    st.success(f"Loaded {len(all_documents)} document(s) from {len(uploaded_files)} PDF(s).")

    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(all_documents)
    st.info(f"Split PDFs into {len(docs)} chunks.")

    # Generate embeddings
    embedder = OllamaEmbeddings(model="mxbai-embed")

    # Create Chroma vector store (auto-persisted)
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embedder,
        persist_directory="chroma_db"  # optional, reload later
    )

    # Setup LLM and Retriever
    llm = OllamaLLM(model="qwen3:4b")
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # Create the RetrievalQA chain properly
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    # ------------------------------
    # Continuous questioning
    st.subheader("Ask questions about your PDF(s)")
    query = st.text_input("Type your question here:")

    if query:
        result = qa.invoke({"query": query})

        # Display answer
        st.subheader("Answer")
        st.write(result["result"])

        # Display sources
        st.subheader("Sources (first 200 characters each)")
        for i, doc in enumerate(result["source_documents"], start=1):
            st.write(f"{i}. {doc.page_content[:200]} ...")
