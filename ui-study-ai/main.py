import streamlit as st
import os
import tempfile
import fitz  # PyMuPDF

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.llms import Ollama
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.chains import RetrievalQA

st.set_page_config(page_title="AI Study Assistant", layout="centered")
st.title("📘 AI Study Assistant")
st.write("Upload your textbook and ask questions to get accurate answers based only on the book.")

# Upload book PDF
book_file = st.file_uploader("📚 Upload Book PDF", type=["pdf"])

# Choose how to input question
question_option = st.radio("How do you want to provide your question?", ["Type manually", "Upload PDF"])
user_question = ""

if question_option == "Type manually":
    user_question = st.text_area("📝 Type your question here:")
else:
    question_pdf = st.file_uploader("📄 Upload Question PDF", type=["pdf"], key="question_pdf")
    if question_pdf:
        doc = fitz.open(stream=question_pdf.read(), filetype="pdf")
        user_question = "\n".join(page.get_text() for page in doc)

# When user clicks the button
if st.button("🔍 Get Answer") and book_file and user_question.strip():

    # Save uploaded book PDF temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(book_file.read())
        tmp_path = tmp.name

    # Load and split PDF
    st.info("🔄 Reading and chunking the book...")
    loader = PyMuPDFLoader(tmp_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # Embed and store in FAISS (in-memory, Streamlit Cloud-friendly)
    st.info("📦 Creating in-memory vector store...")
    embedding = OllamaEmbeddings(model="tinyllama")
    vectordb = FAISS.from_documents(documents=chunks, embedding=embedding)

    # Create RetrievalQA chain
    st.info("🤖 Generating answer...")
    llm = Ollama(model="tinyllama")
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectordb.as_retriever())

    # Get answer
    answer = qa.run(user_question)

    # Show final result
    st.success("✅ Answer Generated")
    st.markdown(f"**Answer:**\n\n{answer}")

    # Clean up
    os.remove(tmp_path)
