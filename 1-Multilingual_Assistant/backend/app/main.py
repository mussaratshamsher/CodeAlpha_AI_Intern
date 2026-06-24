from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.translation import router as translation_router
from app.routes.chatbot import router as chatbot_router


app = FastAPI(title="AI Language Assistant")

# CORS (frontend on different origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(translation_router, prefix="/api", tags=["translation"])
app.include_router(chatbot_router, prefix="/api", tags=["chatbot"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

