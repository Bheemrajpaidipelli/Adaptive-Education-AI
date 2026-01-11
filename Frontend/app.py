import streamlit as st
import requests

st.set_page_config(page_title="EDUAI Student Assistant")

st.title("🎓 EDUAI – Student Learning Assistant")

level = st.selectbox(
    "Select your education level",
    ["School", "Undergraduate", "Postgraduate / Research"]
)

uploaded_file = st.file_uploader(
    "Upload a study document (PDF or TXT)",
    type=["pdf", "txt"]
)

question = st.text_area("Ask your question")

if st.button("Get Answer"):
    if not uploaded_file or not question:
        st.warning("Please upload a file and ask a question.")
    else:
        response = requests.post(
            "http://127.0.0.1:8000/ask",
            data={"question": question, "level": level},
            files={"file": (uploaded_file.name, uploaded_file)}
        )

        if response.status_code != 200:
            st.error("Backend error occurred.")
            st.code(response.text)
        else:
            data = response.json()
            st.subheader("🎯 Answer")
            st.write(data["answer"])
