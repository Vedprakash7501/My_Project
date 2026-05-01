from __future__ import annotations

import json
import os
from urllib import request
from urllib.error import HTTPError, URLError


GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_GROQ_MODEL = "llama-3.1-8b-instant"


class GroqClientError(RuntimeError):
    """Raised when a Groq API call fails."""


def call_groq_chat_completion(
    *,
    prompt_payload: dict[str, object],
    timeout_seconds: float = 20.0,
    max_tokens: int = 800,
    temperature: float = 0.2,
    model: str | None = None,
) -> str:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise GroqClientError("GROQ_API_KEY is missing in environment")

    chosen_model = model or os.getenv("GROQ_MODEL") or DEFAULT_GROQ_MODEL
    system_instruction = str(prompt_payload.get("system_instruction", ""))
    body = {
        "model": chosen_model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": json.dumps(prompt_payload, ensure_ascii=True)},
        ],
    }

    data = json.dumps(body).encode("utf-8")
    req = request.Request(
        GROQ_BASE_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout_seconds) as resp:
            raw = resp.read().decode("utf-8")
    except HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise GroqClientError(f"Groq HTTP error {exc.code}: {details}") from exc
    except URLError as exc:
        raise GroqClientError(f"Groq network error: {exc.reason}") from exc

    parsed = json.loads(raw)
    choices = parsed.get("choices")
    if not isinstance(choices, list) or not choices:
        raise GroqClientError("Groq response missing choices")

    first = choices[0]
    message = first.get("message") if isinstance(first, dict) else None
    content = message.get("content") if isinstance(message, dict) else None
    if not isinstance(content, str) or not content.strip():
        raise GroqClientError("Groq response missing message content")
    return content

