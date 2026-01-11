def build_prompt(question: str, level: str, context: str) -> str:
    if level == "School":
        style = "Explain in very simple words with easy examples."
    elif level == "Undergraduate":
        style = "Explain clearly with concepts and examples."
    else:
        style = "Explain in a detailed, academic, and research-oriented way."

    return f"""
You are an AI assistant for students.

Use the following study material to answer.

Context:
{context}

Instruction:
{style}

Question:
{question}
"""
