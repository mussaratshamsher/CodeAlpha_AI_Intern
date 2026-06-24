# Agents (translator + chatbot)

This folder contains small, single-responsibility agent wrappers for the API routes.

- `llm_client.py`: OpenAI-compatible client configured for Groq (`GROQ_API_KEY`, optional `GROQ_BASE_URL`, `GROQ_MODEL`).
- `translator_agent.py`: translation prompt wrapper.
- `chatbot_agent.py`: support/QA prompt wrapper.

