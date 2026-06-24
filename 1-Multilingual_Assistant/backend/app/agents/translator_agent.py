from dataclasses import dataclass

from .llm_client import chat_completion


TRANSLATION_SYSTEM_PROMPT = (
    "You are a professional multilingual translation assistant. "
    "Translate the user's text from the source language to the target language. "
    "Preserve meaning, grammar, and punctuation. "
    "Return ONLY the translated text (no quotes, no extra commentary)."
)


@dataclass
class TranslatorAgent:
    model: str

    def translate(self, *, text: str, source_lang: str, target_lang: str) -> str:
        messages = [
            {"role": "system", "content": TRANSLATION_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Source language: {source_lang}\n"
                    f"Target language: {target_lang}\n"
                    f"Text: {text}"
                ),
            },
        ]

        return chat_completion(messages=messages, model=self.model, temperature=0.1, max_tokens=1024).strip()

