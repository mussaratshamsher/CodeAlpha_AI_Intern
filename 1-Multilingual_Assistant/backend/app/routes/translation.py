from fastapi import APIRouter
from pydantic import BaseModel, Field


router = APIRouter()


class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to translate")
    source_lang: str = Field("auto", description="Source language code or 'auto'")
    target_lang: str = Field(..., description="Target language code")


class TranslateResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str


@router.post("/translate", response_model=TranslateResponse)
def translate(req: TranslateRequest) -> TranslateResponse:
    from app.agents.translator_agent import TranslatorAgent

    import os

    agent = TranslatorAgent(model=(os.getenv("GROQ_MODEL") or "llama-3.3-70b-versatile").strip())


    translated = agent.translate(
        text=req.text,
        source_lang=req.source_lang,
        target_lang=req.target_lang,
    )

    return TranslateResponse(
        translated_text=translated,
        source_lang=req.source_lang,
        target_lang=req.target_lang,
    )


