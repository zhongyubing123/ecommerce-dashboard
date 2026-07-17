from fastapi import FastAPI
from pydantic import BaseModel

from services.agent_service import run_agent

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat_api(req: ChatRequest):


    answer = run_agent(req.message)

    return {
        "answer": answer
    }