##  EDUAI – Adaptive AI Student Learning Assistant

An intelligent, level-aware educational assistant built using FastAPI, Streamlit, LangGraph, and Retrieval-Augmented Generation (RAG).

## Why EDUAI?

Most AI chatbots provide generic answers.

## EDUAI goes further by:

* Adapting explanation depth based on student level

* Using uploaded documents for context-aware answers

* Structuring reasoning using LangGraph

* Supporting academic validation and refinement

* Following production-style frontend/backend separation

##  System Architecture
# High-Level Flow
User (Streamlit UI)
        │
        ▼
FastAPI Backend
        │
        ├── If file uploaded → RAG Pipeline
        │
        └── If no file → Direct LLM
                │
                ▼
LangGraph Processing
        │
        ├── Internal Validation
        ├── Academic Refinement
        └── Education-Level Adaptation
                │
                ▼
Final Answer to User
## Core Capabilities
1️) Dual Intelligence Mode
Mode	               Trigger	                   Description
LLM Mode	      No file uploaded	       Direct explanation from model
RAG Mode	       File uploaded	       Context retrieved from document using FAISS

2️) Education-Level Adaptation

The same concept is rewritten differently based on:

* School → Simplified explanation

* Undergraduate → Concept-focused

* Postgraduate / Research → Academic depth

3️) Document-Based Question Answering

Supports PDF and TXT

Uses FAISS vector database

Custom word-average embeddings

Top-k semantic retrieval

Context-aware explanation generation

## Technology Stack
# Backend

FastAPI

LangGraph

LangChain

FAISS

Groq API (LLaMA 3.1)

# Frontend

Streamlit

# AI Model
llama-3.1-8b-instant (via Groq)

## Project Structure
EDUAI-Student-Assistant/
│
├── Backend/
│   │
│   ├── main.py                # FastAPI app (API endpoints)
│   ├── graph.py               # LangGraph reasoning pipeline
│   ├── rag.py                 # RAG pipeline (document loading + FAISS)
│   ├── embeddings.py          # Custom WordAverageEmbeddings
│   ├── config.py              # API keys configuration
│   ├── requirements.txt       # Backend dependencies
│   ├── .env                   # Environment variables (NOT pushed to GitHub)
│   │
│   └── __init__.py            # (Optional but recommended)
│
├── Frontend/
│   │
│   ├── app.py                 # Streamlit UI
│   └── requirements.txt       # Frontend dependencies (optional)
│
├── .gitignore
├── README.md
└── LICENSE (optional)

## File-by-File Explanation
# Backend Folder
* main.py

FastAPI app

/ask endpoint

Handles:

File upload (optional)

RAG if file exists

Direct LLM if no file

Returns:

{
  "answer": "Final adapted answer"
}

* graph.py

LangGraph pipeline:

Validate (internal only)

Refine (academic clean-up)

Adapt by education level

Return final answer

Output:

{
    "answer": "... final response ..."
}

* rag.py

Responsible for:

Loading PDF or TXT

Splitting into chunks

Creating FAISS vector DB

Retrieving top-k documents

* embeddings.py

Contains:

class WordAverageEmbeddings


Custom embeddings using word averaging (GloVe or gensim).

* config.py
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

* .env (Important)
GROQ_API_KEY=your_key_here


⚠ Never push this to GitHub.

## Installation & Setup
## 1️ Clone Repository
git clone https://github.com/YOUR_USERNAME/EDUAI-Student-Assistant.git
cd EDUAI-Student-Assistant

## 2️ Install Backend Dependencies
cd Backend
pip install -r requirements.txt

## 3️ Configure API Key

Create a .env file in Backend/:

GROQ_API_KEY=your_api_key_here

## 4️ Run Backend
uvicorn main:app --reload


Server runs at:

http://127.0.0.1:8000

## 5️ Run Frontend

Open a new terminal:

cd Frontend
streamlit run app.py


## App runs at:

http://localhost:5000

## Example Use Cases

* Simplify research concepts
* Explain laboratory techniques
* Convert academic text to school-level
* Resume/document summarization
* Personalized learning assistant

## What Makes This Project Strong?

* Production-style architecture
*Structured reasoning via LangGraph
* Education-aware content transformation
* RAG-enabled contextual intelligence
* Clean frontend/backend separation
* Research-extendable design

## Future Improvements

Conversation memory

Multi-document retrieval

Response streaming

Hallucination detection

Citation generation

Cloud deployment (Render / AWS / HugingFace Spaces)

## Author

Bheemraj Paidipelli
MSc AI & Data Science
Central University of Andhra Pradesh

## License

MIT License
