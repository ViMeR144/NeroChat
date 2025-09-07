from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from ..services.llm import get_llm_client, LLMClient
from ..services.tools import maybe_solve_math
from ..services.prompt import SYSTEM_PROMPT

router = APIRouter()

class Message(BaseModel):
	role: str = Field(..., pattern="^(system|user|assistant)$")
	content: str

class ChatRequest(BaseModel):
	messages: List[Message]
	use_math_tool: bool = False
	model: Optional[str] = None
	max_tokens: int = 192
	temperature: float = 0.2

class ChatResponse(BaseModel):
	answer: str
	finish_reason: Optional[str] = None
	usage: Optional[dict] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest, llm: LLMClient = Depends(get_llm_client)):
	messages = [m.model_dump() for m in req.messages]
	if not any(m.get("role") == "system" for m in messages):
		messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
	if req.use_math_tool:
		tool_result = maybe_solve_math(messages)
		if tool_result:
			messages.append({"role": "assistant", "content": tool_result})

	try:
		result = await llm.chat(messages=messages, model=req.model, max_tokens=req.max_tokens, temperature=req.temperature)
		return ChatResponse(answer=result["answer"], finish_reason=result.get("finish_reason"), usage=result.get("usage"))
	except Exception as e:
		raise HTTPException(status_code=500, detail=f"LLM error: {e}")
