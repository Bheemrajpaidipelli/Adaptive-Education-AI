from fastapi import FastAPI, UploadFile, Form, HTTPException
import tempfile, os

from rag import create_vector_db_from_file
from graph import app_graph

app = FastAPI(title="EDU AI Student Assistant")

@app.post("/ask")
async def ask_student(
    question: str = Form(...),
    level: str = Form(...),
    file: UploadFile = Form(...)
):
    suffix = os.path.splitext(file.filename)[1]

    if suffix not in [".pdf", ".txt"]:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        temp_path = tmp.name

    vector_db = create_vector_db_from_file(temp_path)
    docs = vector_db.similarity_search(question, k=3)
    context = "\n".join([d.page_content for d in docs])

    result = app_graph.invoke({
        "question": question,
        "context": context,
        "level": level
    })

    return {"answer": result["answer"]}
