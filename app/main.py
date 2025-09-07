from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import chat
from .routes import auth as auth_routes
from .routes import history as history_routes
from dotenv import load_dotenv
from .db import engine, Base

load_dotenv()

app = FastAPI(title="Bilingual QA LLM Server", version="0.2.0")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
	Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router, prefix="/api")
app.include_router(history_routes.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/")
async def root():
	return {"status": "ok", "service": "bilingual-qa-llm"}
