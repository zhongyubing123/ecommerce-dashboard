from fastapi import FastAPI
from pydantic import BaseModel
from services.deepseek_service import chat

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat_api(req: ChatRequest):
    answer = chat(req.message)

    return {
        "answer": answer
    }