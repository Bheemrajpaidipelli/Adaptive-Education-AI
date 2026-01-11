from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from typing import TypedDict
from config import GROQ_API_KEY

# 1️⃣ Define explicit state schema
class GraphState(TypedDict):
    question: str
    context: str
    level: str
    answer: str

# 2️⃣ Initialize LLM
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.3
)

# 3️⃣ Node logic
def generate_answer(state: GraphState):
    question = state.get("question", "")
    context = state.get("context", "")
    level = state.get("level", "General")

    prompt = f"""
You are an AI student assistant.

Education level: {level}

Context:
{context}

Question:
{question}

Explain clearly and simply based on the student's level.
"""

    response = llm.invoke(prompt)

    return {"answer": response.content}

# 4️⃣ Build graph
graph = StateGraph(GraphState)
graph.add_node("answer", generate_answer)
graph.set_entry_point("answer")

app_graph = graph.compile()
