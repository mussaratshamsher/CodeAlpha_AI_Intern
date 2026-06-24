from fastapi import APIRouter
from pydantic import BaseModel, Field


router = APIRouter()


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)


class ChatResponse(BaseModel):
    answer: str
    used: str = Field("faq", description="faq | groq")


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    from app.agents.chatbot_agent import ChatbotAgent
    import os

    agent = ChatbotAgent(model=(os.getenv("GROQ_MODEL") or "llama-3.3-70b-versatile").strip())
    answer = agent.answer(question=req.question)

    return ChatResponse(answer=answer, used="groq")


