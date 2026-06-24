from dataclasses import dataclass

from .llm_client import chat_completion


CHAT_SYSTEM_PROMPT = (
    "You are an AI assistant for multilingual product/support questions. "
    "Answer clearly and concisely. "
    "If you are unsure, say so and ask a clarifying question. "
)


@dataclass
class ChatbotAgent:
    model: str

    def answer(self, *, question: str) -> str:
        messages = [
            {"role": "system", "content": CHAT_SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ]

        return chat_completion(messages=messages, model=self.model, temperature=0.2, max_tokens=512).strip()

