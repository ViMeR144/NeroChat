# Bilingual QA LLM Server

Minimal FastAPI server that proxies to an OpenAI-compatible LLM (OpenRouter or self-hosted vLLM), with optional simple math evaluation. Supports Russian and English.

## Backend (FastAPI)

1. Create and activate venv:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```
2. Install deps:
```powershell
pip install -r requirements.txt
```
3. Set env vars (PowerShell):
```powershell
$env:OPENAI_BASE_URL = "
https://openrouter.ai/api/v1"
$env:OPENAI_API_KEY = "sk-REPLACE"
$env:LLM_MODEL = "openrouter/anthropic/claude-3.5-sonnet"
```
4. Run server:
```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Frontend (React + Vite)

1. Install deps:
```powershell
cd web
npm install
```
2. Start dev server (proxy to backend at http://localhost:8000):
```powershell
npm run dev
```
Open http://localhost:5173/ in your browser.

## Docker (Backend)

Build and run:
```bash
docker build -t bilingual-qa .
docker run -e OPENAI_BASE_URL -e OPENAI_API_KEY -e LLM_MODEL -p 8000:8000 bilingual-qa
```

## Self-hosted LLM via vLLM

- Launch vLLM with OpenAI API:
```bash
python -m vllm.entrypoints.openai.api_server --model meta-llama/Meta-Llama-3-8B-Instruct --port 8001
```
- Set:
```powershell
$env:OPENAI_BASE_URL = "http://localhost:8001/v1"
$env:OPENAI_API_KEY = "EMPTY"
$env:LLM_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"
```

## Notes
- Math tool handles simple numeric expressions; LLM handles everything else.
- Extend with tools/RAG via `app/services/tools.py` and `app/routes/chat.py`.
