from fastapi import FastAPI, UploadFile, Form
import tempfile, os, traceback

from rag import create_vector_db_from_file
from graph import app_graph

app = FastAPI(title="EDUAI Student Assistant")

@app.post("/ask")
async def ask_student(
    question: str = Form(...),
    level: str = Form(...),
    file: UploadFile = Form(...)
):
    try:
        suffix = os.path.splitext(file.filename)[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            temp_path = tmp.name

        #print("📄 Temp file saved:", temp_path)

        vector_db = create_vector_db_from_file(temp_path)
        #print("✅ Vector DB created")

        docs = vector_db.similarity_search(question, k=3)
        #print("📚 Retrieved docs:", len(docs))

        context = "\n".join(d.page_content for d in docs)

        result = app_graph.invoke({
            "question": question,
            "context": context,
            "level": level
        })

        #print("🧠 Graph result:", result)

        return {"answer": result["answer"]}

    except Exception as e:
        print("❌ ERROR OCCURRED")
        traceback.print_exc()
        return {"error": str(e)}
