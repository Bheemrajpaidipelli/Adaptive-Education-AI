import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from embeddings import WordAverageEmbeddings

def create_vector_db_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError("Unsupported file type")

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(documents)

    texts = [chunk.page_content for chunk in chunks]

    embeddings = WordAverageEmbeddings()
    vectors = embeddings.embed_documents(texts)

    vector_db = FAISS.from_embeddings(
        list(zip(texts, vectors)),
        embedding=embeddings
    )

    return vector_db
