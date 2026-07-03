---
title: AI Music Generator
emoji: 🎵
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# 🎵 AI Music Generator

AI-powered music generation using:

- FastAPI
- TensorFlow LSTM
- MIDI Generation
- WAV Audio Conversion
- REST API

## API Endpoints

### Generate Music

POST

```bash
/generate
```

Request:

```json
{
  "seed_notes": "C4 E4 G4",
  "length": 128,
  "temperature": 1.0,
  "filename": "track.mid"
}
```

Response:

```json
{
  "midi_url": "/files/track.mid",
  "audio_url": "/files/track.wav"
}
```

### Access Files

```bash
/files/{filename}
```

## Frontend

Recommended frontend deployment:

- Vercel

Backend:

- Hugging Face Spaces (Docker)
