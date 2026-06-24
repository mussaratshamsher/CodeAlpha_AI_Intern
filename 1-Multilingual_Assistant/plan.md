# AI Language Assistant (Portfolio Version)

## Project Vision

Build a portfolio-ready AI application that combines:

### 1. AI Translator

* Multi-language translation
* Source & target language selection
* Copy translated text
* Translation history

### 2. Semantic FAQ Chatbot

* NLP preprocessing
* Embeddings generation
* FAISS vector search
* Groq fallback responses
* Chat-style interface

This project demonstrates:

* FastAPI
* NLP
* Embeddings
* Vector Search
* FAISS
* LLM Integration
* REST APIs
* Frontend Development
* Testing
* Deployment

---

# Technology Stack

## Frontend

* HTML5
* CSS3
* Vanilla JavaScript

## Backend

* FastAPI
* Python

## AI & NLP

* Groq API
* NLTK
* Sentence Transformers
* Scikit-Learn
* FAISS

## Storage

* FAQ JSON
* Local FAISS Index

## Deployment

* Render (Backend)
* Vercel or GitHub Pages (Frontend)

---

# Project Structure

```text
AI-Language-Assistant/

backend/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── translation.py
│   │   └── chatbot.py
│   │
│   ├── services/
│   │   ├── translator_service.py
│   │   ├── faq_service.py
│   │   ├── embedding_service.py
│   │   ├── faiss_service.py
│   │   └── groq_service.py
│   │
│   ├── data/
│   │   ├── faq.json
│   │   ├── faq_embeddings.npy
│   │   └── faq_index.faiss
│   │
│   ├── tests/
│   │   ├── test_translation.py
│   │   ├── test_chatbot.py
│   │   └── test_api.py
│   │
│   └── utils/
│       └── preprocess.py
│
├── requirements.txt
└── .env

frontend/
│
├── index.html
├── style.css
├── script.js
└── assets/
```

---

# PHASE 1 — Foundation & Architecture

## Objective

Set up the complete project structure and backend foundation.

### Tasks

* Create GitHub repository.
* Configure FastAPI project.
* Configure CORS.
* Configure Groq API.
* Create frontend skeleton.
* Create reusable API client functions.

### Deliverables

* Backend running.
* Frontend running.
* API connectivity confirmed.

### Tests

Backend:

```bash
uvicorn app.main:app --reload
```

Expected:

```text
localhost:8000/docs
```

loads successfully.

### GitHub Commit

```text
Phase 1 - Project Foundation
```

---

# PHASE 2 — AI Translation Module

## Objective

Develop the complete translation feature.

### Tasks

Backend

* Create translation endpoint.
* Integrate Groq API.
* Add language validation.
* Add error handling.

Frontend

* Translation form.
* Source language dropdown.
* Target language dropdown.
* Translate button.
* Result display.
* Copy button.

### API

```text
POST /api/translate
```

### Tests

Test 1

Input:

```text
Hello World
```

Expected:

Urdu translation returned.

Test 2

Empty input.

Expected:

Validation error.

Test 3

Long paragraph translation.

Expected:

Successful response.

### GitHub Commit

```text
Phase 2 - Translation Module Complete
```

---

# PHASE 3 — NLP Pipeline & Vector Search

## Objective

Build semantic search infrastructure.

### Tasks

Create FAQ dataset:

```text
faq.json
```

Add:

* 30–50 FAQs

Implement:

* Lowercasing
* Tokenization
* Stopword removal

Generate embeddings using:

```python
all-MiniLM-L6-v2
```

Create:

```text
faq_embeddings.npy
```

Create FAISS index:

```text
faq_index.faiss
```

### Workflow

```text
FAQ Data
   ↓
Preprocessing
   ↓
Embeddings
   ↓
FAISS Index
```

### Tests

Query:

```text
How do I contact support?
```

Expected:

Matches relevant FAQ.

Similarity threshold:

```python
0.70
```

### GitHub Commit

```text
Phase 3 - NLP and FAISS Search
```

---

# PHASE 4 — FAQ Chatbot Module

## Objective

Create chatbot functionality using vector search.

### Tasks

Create:

```text
POST /api/chat
```

Flow:

```text
User Question
      ↓
Embedding
      ↓
FAISS Search
      ↓
Best Match
      ↓
Return Answer
```

Frontend

* Chat window
* User bubbles
* Bot bubbles
* Auto-scroll

### Tests

FAQ Question

Expected:

Correct FAQ answer.

Unknown Question

Expected:

Low similarity score detected.

### GitHub Commit

```text
Phase 4 - Semantic FAQ Chatbot
```

---

# PHASE 5 — AI Fallback & UX Improvements

## Objective

Make chatbot intelligent beyond FAQs.

### Tasks

If similarity score:

```python
< 0.70
```

then:

```text
Send question to Groq
```

Return AI-generated answer.

Add:

* Loading spinner
* Toast messages
* Copy translation
* Translation history
* Responsive design

Optional

* Text-to-Speech
* Voice Input

### Workflow

```text
Question
    ↓
FAISS Search
    ↓
Found?
 ┌───────┐
 │ Yes   │
 └───┬───┘
     ↓
 FAQ Answer

No
 ↓
Groq
 ↓
AI Response
```

### Tests

Known FAQ

Expected:

FAQ answer.

Unknown Question

Expected:

Groq response.

### GitHub Commit

```text
Phase 5 - AI Hybrid Chatbot
```

---

# PHASE 6 — Testing, Deployment & Portfolio Polish

## Objective

Prepare production-ready project.

### Backend Tests

Create:

```text
test_translation.py
test_chatbot.py
test_api.py
```

Run:

```bash
pytest
```

Expected:

All tests pass.

---

## Integration Testing

### Translation Workflow

Input

```text
Hello
```

Expected

```text
Translated output displayed
```

---

### FAQ Workflow

Input

```text
What services do you provide?
```

Expected

```text
FAQ answer returned
```

---

### AI Workflow

Input

```text
Explain machine learning
```

Expected

```text
Groq-generated answer
```

---

## Deployment

### Backend

Hugging Face

Environment Variable:

```env
GROQ_API_KEY=
```

### Frontend

Vercel

or

GitHub Pages

---

## Portfolio Deliverables

### GitHub Repository

* Clean README
* Screenshots
* Architecture Diagram
* API Documentation

### Resume Bullet

Built an AI Language Assistant using FastAPI, FAISS Vector Search, Sentence Transformers, NLP preprocessing, and Groq LLM integration, combining semantic FAQ retrieval and multilingual translation into a single intelligent application.

### Final GitHub Commit

```text
Phase 6 - Production Ready Release
```

---

# Final Outcome

A single portfolio project demonstrating:

✓ FastAPI Backend

✓ AI Translation

✓ NLP Preprocessing

✓ Sentence Transformers

✓ Vector Embeddings

✓ FAISS Search

✓ Semantic Retrieval

✓ Groq LLM Integration

✓ Chatbot Development

✓ Frontend Development

✓ Automated Testing

✓ Deployment

✓ RAG Foundations
