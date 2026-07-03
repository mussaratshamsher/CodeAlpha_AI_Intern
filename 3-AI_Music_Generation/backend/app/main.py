from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os
from typing import Optional

app = FastAPI(title="MusicGen AI (MIDI Generator)", version="0.1.0")


# CORS for local dev / static frontend
# If you serve frontend from another port (e.g. file:// or 5500), browsers require explicit allow-list.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[  "http://127.0.0.1:5500",
    "https://ms-music-generation.vercel.app/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)  # .../3-AI_Music_Generation

FRONTEND_DIR = os.path.join(PROJECT_DIR, "frontend")
MODEL_DIR = os.path.join(PROJECT_DIR, "models")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "outputs")
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

class GenerateRequest(BaseModel):
    # For portfolio/demo:
    # If a model is present, it can generate. Otherwise we return a demo MIDI.
    seed_notes: Optional[str] = None  # e.g. "C4 E4 G4 A4"
    length: int = 128
    temperature: float = 1.0
    filename: str = "generated.mid"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def home():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if not os.path.exists(index_path):
        return JSONResponse({"error": "frontend/index.html not found"}, status_code=404)
    return FileResponse(index_path)

@app.get("/files/{file_path:path}")
def files(file_path: str):
    # Prevent path traversal by resolving within OUTPUT_DIR
    safe_base = os.path.abspath(OUTPUT_DIR)
    target = os.path.abspath(os.path.join(OUTPUT_DIR, file_path))
    if not target.startswith(safe_base + os.sep) and target != safe_base:
        return JSONResponse(status_code=400, content={"error": "Invalid file path"})
    if not os.path.exists(target):
        return JSONResponse(status_code=404, content={"error": "File not found"})
    # Let FastAPI/Starlette infer correct mime types.
    return FileResponse(target)


@app.post("/generate")
def generate(req: GenerateRequest):
    from .audio_utils import ensure_wav_from_midi
    from .generation import generate_midi  # local import to keep startup fast

    try:
        # 1) Generate MIDI file on disk
        midi_path = generate_midi(
            seed_notes=req.seed_notes,
            length=req.length,
            temperature=req.temperature,
            output_dir=OUTPUT_DIR,
            filename=req.filename,
        )

        midi_filename = os.path.basename(midi_path)
        midi_basename, _ = os.path.splitext(midi_filename)

        # 2) Convert MIDI->WAV (preferred for browser HTML5 Audio)
        wav_path = ensure_wav_from_midi(
            midi_path,
            out_dir=OUTPUT_DIR,
            output_basename=midi_basename,
        )
        wav_filename = os.path.basename(wav_path)

        # 3) Return URLs for frontend to play + download
        # Use relative URLs so it works behind reverse proxies / different host.
        midi_url = f"/files/{midi_filename}"
        audio_url = f"/files/{wav_filename}"

        return JSONResponse(
            content={
                "id": midi_basename,
                "midi_url": midi_url,
                "audio_url": audio_url,
                "midi_filename": midi_filename,
                "audio_filename": wav_filename,
                "seed_notes": req.seed_notes,
                "length": req.length,
                "temperature": req.temperature,
            }
        )
    except Exception as e:
        # Include traceback for easier debugging in local dev
        import traceback
        tb = traceback.format_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "type": e.__class__.__name__,
                "traceback": tb,
            },
        )


