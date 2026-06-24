# AI Language Assistant (Portfolio-ready)

Multilingual translation + semantic FAQ chatbot built with FastAPI, Sentence Transformers, FAISS, and Groq.

## Quick start (backend)

1) Create virtual environment and install dependencies

```bash
cd backend
python -m venv .venv
.
```

2) Install requirements

```bash
pip install -r requirements.txt
```

3) Set `GROQ_API_KEY` in `.env`

4) Run

```bash
uvicorn app.main:app --reload
```

Open: http://localhost:8000/docs

## Frontend
Serve static files or deploy via Vercel/GitHub Pages.

- `frontend/index.html`
- Talks to backend via `/api/*`.

