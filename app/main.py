from fastapi import FastAPI
from pydantic import BaseModel
from app.answer import answer_incident

app = FastAPI()

class AskReq(BaseModel):
    incident_text: str

@app.post("/ask")
def ask(req: AskReq):
    return answer_incident(req.incident_text)