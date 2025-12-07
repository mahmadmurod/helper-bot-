"""
dev2 to be implement description later
"""

from abc import ABC, abstractmethod
from typing import Optional
import httpx
import asyncio
from backend.utils.logger import logger
from backend.config import settings
from backend.models.enums import AIProvider


class AIAdapter(ABC):
    @abstractmethod
    async def generate(self, prompt: str) -> str:
        raise NotImplementedError


class MockAIAdapter(AIAdapter):
    async def generate(self, prompt: str) -> str:
        await asyncio.sleep(0.01)
        return f"[mock] {prompt[:200]}"


class HTTPAIAdapter(AIAdapter):
    def __init__(self, url: str, api_key: Optional[str], provider_name: str):
        self.url = url
        self.api_key = api_key
        self.provider_name = provider_name
        self._client = httpx.AsyncClient(timeout=30.0)

    async def _post(self, payload: dict) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        retries = 3
        backoff = 0.5
        for attempt in range(1, retries + 1):
            try:
                resp = await self._client.post(self.url, json=payload, headers=headers)
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code
                if 400 <= status < 500:
                    logger.error("[%s] client error %s: %s", self.provider_name, status, exc.response.text)
                    raise
                logger.warning("[%s] transient HTTP error attempt %d/%d", self.provider_name, attempt, retries)
            except (httpx.NetworkError, httpx.TimeoutException) as exc:
                logger.warning("[%s] network error attempt %d/%d: %s", self.provider_name, attempt, retries, exc)
            await asyncio.sleep(backoff * attempt)
        raise RuntimeError(f"{self.provider_name} failed after retries")

    async def generate(self, prompt: str) -> str:
        payload = {
            "model": "gpt-4-0613",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512,
        }
        data = await self._post(payload)
        # Common shapes: OpenAI chat completions
        if "choices" in data and isinstance(data["choices"], list) and data["choices"]:
            choice = data["choices"][0]
            if isinstance(choice, dict):
                msg = choice.get("message", {}) or {}
                return msg.get("content") or choice.get("text") or ""
        return data.get("text") or data.get("reply") or ""


def get_default_adapter() -> AIAdapter:
    if settings.OPENAI_API_KEY and settings.OPENAI_API_URL:
        return HTTPAIAdapter(str(settings.OPENAI_API_URL), settings.OPENAI_API_KEY, AIProvider.OPENAI.value)
    if settings.GEMINI_API_KEY and settings.GEMINI_API_URL:
        return HTTPAIAdapter(str(settings.GEMINI_API_URL), settings.GEMINI_API_KEY, AIProvider.GEMINI.value)
    if settings.DEEPSEEK_API_KEY and settings.DEEPSEEK_API_URL:
        return HTTPAIAdapter(str(settings.DEEPSEEK_API_URL), settings.DEEPSEEK_API_KEY, AIProvider.DEEPSEEK.value)
    return MockAIAdapter()
