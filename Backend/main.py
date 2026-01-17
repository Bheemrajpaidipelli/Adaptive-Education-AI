from fastapi import FastAPI, UploadFile, Form
from typing import Optional
import tempfile, os

from rag import create_vector_db_from_file
from graph import app_graph

app = FastAPI(title="EDUAI Student Assistant")

@app.post("/ask")
async def ask_student(
    question: str = Form(...),
    level: str = Form(...),
    file: Optional[UploadFile] = None
):
    context = ""

    # ---------------------------
    # CASE 1: FILE UPLOADED → RAG
    # ---------------------------
    if file:
        suffix = os.path.splitext(file.filename)[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name

        vector_db = create_vector_db_from_file(temp_path)
        docs = vector_db.similarity_search(question, k=3)
        context = "\n".join([d.page_content for d in docs])

    # ---------------------------
    # CASE 2: NO FILE → LLM ONLY
    # ---------------------------
    result = app_graph.invoke({
        "question": question,
        "context": context,   # empty string is OK
        "level": level
    })

    return {
        "answer": result["answer"]
    }
