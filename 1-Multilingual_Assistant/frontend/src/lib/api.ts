// Backend API base URL - HuggingFace Space
const API_BASE = process.env.NEXT_BACKEND_API_URL || "https://mussarat123shamsher-language-assistant.hf.space";

// API endpoints
const ENDPOINTS = {
  chat: "/api/chat",
  translate: "/api/translate",
  health: "/health",
} as const;

// Request/Response types
interface TranslateRequest {
  text: string;
  source_lang: string;
  target_lang: string;
}

interface TranslateResponse {
  translated_text: string;
  source_lang: string;
  target_lang: string;
}

interface ChatRequest {
  question: string;
}

interface ChatResponse {
  answer: string;
  used: string;
}

// API functions

/**
 * Translate text from source language to target language
 */
export async function translateText(req: TranslateRequest): Promise<TranslateResponse> {
  const resp = await fetch(`${API_BASE}${ENDPOINTS.translate}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });

  if (!resp.ok) {
    const error = await resp.text().catch(() => "");
    throw new Error(`Translation failed (${resp.status}): ${error}`);
  }

  return resp.json();
}

/**
 * Send a chat question and get AI response
 */
export async function sendChat(question: string): Promise<ChatResponse> {
  const resp = await fetch(`${API_BASE}${ENDPOINTS.chat}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  if (!resp.ok) {
    const error = await resp.text().catch(() => "");
    throw new Error(`Chat failed (${resp.status}): ${error}`);
  }

  return resp.json();
}

/**
 * Check backend health status
 */
export async function checkHealth(): Promise<{ status: string }> {
  const resp = await fetch(`${API_BASE}${ENDPOINTS.health}`);

  if (!resp.ok) {
    throw new Error(`Health check failed (${resp.status})`);
  }

  return resp.json();
}

// Export types for external use
export type { TranslateRequest, TranslateResponse, ChatRequest, ChatResponse };