# Hugging Face Spaces (Docker) - Backend

Build/run locally:

```bash
cd backend
docker build -t multilingual-backend .
docker run --rm -p 7860:7860 \
  -e GROQ_API_KEY=YOUR_KEY \
  -e GROQ_MODEL=llama-3.3-70b-versatile \
  multilingual-backend
```

Deployment notes:
- Provide `GROQ_API_KEY` in Spaces secrets.
- Optionally set `GROQ_MODEL`.
- Container listens on `${PORT}` (default 7860). 

