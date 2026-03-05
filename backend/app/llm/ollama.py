"""Ollama client with streaming support."""
from __future__ import annotations

import json
from typing import Any, AsyncIterator, Dict, Optional

import httpx

from app.core.config import Settings, get_settings
from app.llm.base import LLMClient, LLMError, LLMResponseChunk
from app.llm.token_estimate import pick_context_window


class OllamaClient(LLMClient):
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.base_url = self.settings.ollama_base_url.rstrip("/")

    async def generate(
        self,
        prompt: str,
        *,
        model: str,
        stream: bool = True,
        max_context: Optional[int] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> AsyncIterator[LLMResponseChunk]:
        num_ctx = max_context or pick_context_window(self.settings.ollama_context_window, prompt)
        payload: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": {"num_ctx": num_ctx},
        }
        if options:
            payload["options"].update(options)

        url = f"{self.base_url}/api/generate"
        timeout = httpx.Timeout(self.settings.ollama_timeout, connect=self.settings.ollama_timeout)

        async with httpx.AsyncClient(timeout=timeout) as client:
            if not stream:
                resp = await client.post(url, json=payload)
                if resp.status_code != 200:
                    raise LLMError(f"Ollama error {resp.status_code}: {resp.text}")
                data = resp.json()
                yield LLMResponseChunk(
                    text=data.get("response", ""),
                    done=True,
                    model=data.get("model"),
                    raw=data,
                )
                return

            async with client.stream("POST", url, json=payload) as stream_resp:
                if stream_resp.status_code != 200:
                    text = await stream_resp.aread()
                    raise LLMError(f"Ollama stream error {stream_resp.status_code}: {text.decode()}")
                async for line in stream_resp.aiter_lines():
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    chunk_text = data.get("response", "")
                    yield LLMResponseChunk(
                        text=chunk_text,
                        done=bool(data.get("done", False)),
                        model=data.get("model"),
                        raw=data,
                    )
