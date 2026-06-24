import os
from typing import Any, Dict, Optional

import httpx
from openai import OpenAI


def _disable_proxy():
    """Disable proxy by removing env vars."""
    for _var in ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy"]:
        os.environ.pop(_var, None)
        os.environ.pop(_var.lower(), None)


def get_groq_client() -> OpenAI:
    """Create an OpenAI-compatible client pointed at Groq."""
    # Disable proxy first
    _disable_proxy()

    # Load .env for local dev
    try:
        from dotenv import load_dotenv
        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"), override=True)
    except Exception:
        pass

    # Disable proxy again after loading .env
    _disable_proxy()

    api_key = (os.getenv("GROQ_API_KEY") or "").strip()
    if not api_key:
        raise RuntimeError(
            "Missing GROQ_API_KEY. Set it as an env var (Spaces secret) or create backend/.env with GROQ_API_KEY."
        )

    base_url = (os.getenv("GROQ_BASE_URL") or "https://api.groq.com/openai/v1").strip()

    # Create httpx client with proxies=None (httpx 0.27.0 supports this)
    http_client = httpx.Client(proxies=None, trust_env=False, timeout=60.0)

    return OpenAI(
        api_key=api_key,
        base_url=base_url,
        http_client=http_client,
    )


def chat_completion(
    *,
    messages: list[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.2,
    max_tokens: int = 512,
) -> str:
    """Call Groq using OpenAI Chat Completions API semantics."""
    client = get_groq_client()
    chosen_model = (model or os.getenv("GROQ_MODEL") or "llama-3.3-70b-versatile").strip()

    resp = client.chat.completions.create(
        model=chosen_model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    return resp.choices[0].message.content or ""

