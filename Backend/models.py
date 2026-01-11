from pydantic import BaseModel

class StudentQuery(BaseModel):
    question: str
    level: str
