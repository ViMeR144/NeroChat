import os
from typing import Any, Dict, List, Optional
import httpx
from pydantic import BaseModel

DEFAULT_MODEL = os.getenv("LLM_MODEL", "anthropic/claude-3.5-sonnet")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_REF = os.getenv("OPENROUTER_HTTP_REFERER", "http://localhost:5173")
OPENROUTER_TITLE = os.getenv("OPENROUTER_X_TITLE", "NeoChat")

class LLMClient:
	async def chat(self, messages: List[Dict[str, str]], model: Optional[str] = None, max_tokens: int = 512, temperature: float = 0.2) -> Dict[str, Any]:
		raise NotImplementedError

class OpenAICompatibleClient(LLMClient):
	def __init__(self, base_url: str, api_key: str, default_model: str):
		self.base_url = base_url.rstrip("/")
		self.api_key = api_key
		self.default_model = default_model
		self._client = httpx.AsyncClient(timeout=300)

	async def chat(self, messages: List[Dict[str, str]], model: Optional[str] = None, max_tokens: int = 512, temperature: float = 0.2) -> Dict[str, Any]:
		payload = {
			"model": model or self.default_model,
			"messages": messages,
			"max_tokens": max_tokens,
			"temperature": temperature,
		}
		headers = {
			"Authorization": f"Bearer {self.api_key}",
			"Content-Type": "application/json",
			# OpenRouter extras
			"HTTP-Referer": OPENROUTER_REF,
			"X-Title": OPENROUTER_TITLE,
		}
		try:
			resp = await self._client.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
			resp.raise_for_status()
			data = resp.json()
			choice = data["choices"][0]
			return {
				"answer": choice["message"]["content"],
				"finish_reason": choice.get("finish_reason"),
				"usage": data.get("usage"),
			}
		except httpx.HTTPStatusError as exc:
			body = exc.response.text
			raise RuntimeError(f"OpenAI-compatible API error {exc.response.status_code}: {body}")

async def get_llm_client() -> LLMClient:
	base_url = OPENAI_BASE_URL
	api_key = OPENAI_API_KEY
	model = DEFAULT_MODEL
	if not api_key:
		raise RuntimeError("OPENAI_API_KEY is not set. Configure your API key in environment or .env file.")
	return OpenAICompatibleClient(base_url=base_url, api_key=api_key, default_model=model)
