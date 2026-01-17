import streamlit as st
import requests

st.set_page_config(page_title="EDUAI Student Assistant")

st.title("🎓 EDUAI – Student Learning Assistant")

level = st.selectbox(
    "Select your education level",
    ["School", "Undergraduate", "Postgraduate / Research"]
)

uploaded_file = st.file_uploader(
    "Upload a study document (PDF or TXT) (Optional)",
    type=["pdf", "txt"]
)

question = st.text_area("Ask your question")

if st.button("Get Answer"):

    # ✅ Only question is mandatory
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                # 🔹 Case 1: File uploaded → RAG + LLM
                if uploaded_file is not None:
                    response = requests.post(
                        "http://127.0.0.1:8000/ask",
                        data={
                            "question": question,
                            "level": level
                        },
                        files={
                            "file": (uploaded_file.name, uploaded_file)
                        }
                    )

                # 🔹 Case 2: No file → LLM only
                else:
                    response = requests.post(
                        "http://127.0.0.1:8000/ask",
                        data={
                            "question": question,
                            "level": level
                        }
                    )

                if response.status_code != 200:
                    st.error("Backend error occurred.")
                    st.code(response.text)
                else:
                    data = response.json()
                    st.subheader("🎯 Answer")
                    st.write(data.get("answer", "No answer returned"))
                    
            except Exception as e:
                st.error("Failed to connect to backend.")
                st.code(str(e))
