from typing import TypedDict
from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from config import GROQ_API_KEY

# ---------- State Definition ----------
class GraphState(TypedDict):
    question: str
    context: str   # may be empty
    level: str
    answer: str


# ---------- LLM ----------
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.3
)

# ---------- Nodes ----------
def validate_explanation(state: GraphState):
    """
    Internal validation (silent, not exposed)
    Works for both RAG and non-RAG
    """
    text = state["context"] if state["context"].strip() else state["question"]

    prompt = f"""
You are an academic evaluator.

Check whether the following explanation is conceptually correct.
Mention strengths and briefly point out if anything important is missing.

Explanation:
{text}
"""
    llm.invoke(prompt)
    return {}  # intentionally discard output


def refine_explanation(state: GraphState):
    """
    Internal academic refinement
    """
    text = state["context"] if state["context"].strip() else state["question"]

    prompt = f"""
Rewrite the explanation below to be:
- Clear and concise
- Academic in tone
- Plagiarism-safe
- Suitable for assignments

Do NOT add new information.

Text:
{text}
"""
    response = llm.invoke(prompt)
    return {"context": response.content}


def adapt_by_level(state: GraphState):
    """
    FINAL user-visible answer
    """
    prompt = f"""
Rewrite the explanation below for a student at this level:
{state["level"]}

Rules:
- Adjust depth and vocabulary
- Keep meaning unchanged
- Be easy to understand

Text:
{state["context"]}
"""
    response = llm.invoke(prompt)
    return {"answer": response.content}


# ---------- Graph ----------
graph = StateGraph(GraphState)

graph.add_node("validate", validate_explanation)
graph.add_node("refine", refine_explanation)
graph.add_node("adapt", adapt_by_level)

graph.set_entry_point("validate")
graph.add_edge("validate", "refine")
graph.add_edge("refine", "adapt")

app_graph = graph.compile()
