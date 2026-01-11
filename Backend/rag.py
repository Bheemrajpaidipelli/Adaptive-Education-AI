import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from embeddings import WordAverageEmbeddings

def create_vector_db_from_file(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")

    documents = loader.load()

    if not documents or not any(d.page_content.strip() for d in documents):
        raise ValueError("Uploaded file contains no readable text.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)
    chunks = [c for c in chunks if len(c.page_content.strip()) > 50]

    if not chunks:
        raise ValueError("Document text could not be split into valid chunks.")

    embedding = WordAverageEmbeddings()

    vector_db = FAISS.from_texts(
        texts=[c.page_content for c in chunks],
        embedding=embedding
    )

    return vector_db
