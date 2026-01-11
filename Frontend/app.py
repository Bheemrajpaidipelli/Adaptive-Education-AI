import streamlit as st
import requests

st.set_page_config(page_title="AI Student Assistant")

st.title("🎓 AI Student Assistant")

level = st.selectbox(
    "Select your education level",
    ["School", "Undergraduate", "Postgraduate / Research"]
)

uploaded_file = st.file_uploader(
    "Upload study material (PDF or TXT)",
    type=["pdf", "txt"]
)

question = st.text_area("Ask your question")

if st.button("Get Answer"):
    if not uploaded_file or not question:
        st.warning("Please upload a file and ask a question.")
    else:
        files = {
            "file": (uploaded_file.name, uploaded_file, uploaded_file.type)
        }

        data = {
            "question": question,
            "level": level
        }

        res = requests.post(
            "http://127.0.0.1:8000/ask",
            files=files,
            data=data
        )

        if res.status_code == 200:
            st.success("Answer")
            st.write(res.json()["answer"])
        else:
            st.error(res.text)
