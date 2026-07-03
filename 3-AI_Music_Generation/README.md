# 🎵 MusicGen AI — AI-Powered MIDI Composer

Generate new melodies as **MIDI** from a seed (placeholder generator now; LSTM wiring ready for later).

---

## What it includes
- **FastAPI backend** (`POST /generate`) that returns a `.mid`
- **Clean HTML UI** (`frontend/index.html`) styled with **Tailwind + AOS** (animations)
- MIDI writing via **pretty_midi**

---

## Demo UI
Open: `http://localhost:8000/` after starting the server.

---

## How to run locally
### 1) Install
```bash
pip install -r 3-AI_Music_Generation/requirements.txt
```

### 2) Start backend
```bash
uvicorn app.main:app --reload --port 8000
```

### 3) Use the UI
- Go to `/` in your browser
- Enter seed notes like: `C4 E4 G4 A4`
- Click **Generate** → then **Download**

---

## API
- `GET /health` → `{ "status": "ok" }`
- `POST /generate`
  - body: `seed_notes` (string, optional), `length` (int), `temperature` (float), `filename` (string)
  - response: generated `.mid` file

---

## Project structure
```text
3-AI_Music_Generation/
├── backend/app/main.py
├── backend/app/generation.py
├── frontend/index.html
├── outputs/
└── requirements.txt
```

---

## Next steps (for full AI training)
- Implement MIDI → sequences preprocessing with `music21`
- Train an **LSTM** model on note sequences (`tensorflow/keras`)
- Replace the placeholder generator with real model-based generation
