# Latest, non-deprecated imports
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import RetrievalQA

# ------------------------------
# 1️⃣ Load PDF
print("\nLoad PDF")
pdf_path = "data/example.pdf"  # replace with your PDF path
loader = PyPDFLoader(pdf_path)
documents = loader.load()

# ------------------------------
# 2️⃣ Split into chunks
print("\nSplit into chunks")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100
)
docs = text_splitter.split_documents(documents)

# ------------------------------
# 3️⃣ Generate embeddings
embedder = OllamaEmbeddings(model="mxbai-embed-large:latest")

# ------------------------------
# 4️⃣ Create Chroma vector store (auto-persistence)
print("\nCreate Chroma vector store")
vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embedder,
    persist_directory="chroma_db"  # optional, for reloading later
)

# ------------------------------
# 5️⃣ Setup Retriever + LLM
llm = OllamaLLM(model="qwen3:4b")

print("\nRetriever data")
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# ------------------------------
# 6️⃣ Ask a question
query = input("Enter your question about the PDF: ")

# Use the new recommended method
result = qa.invoke({"query": query})

print("\nAnswer:")
print(result["result"])
