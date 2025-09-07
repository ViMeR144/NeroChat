from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..db import get_db
from ..models import User, Conversation, Message
from ..auth import get_current_user_email

router = APIRouter(prefix="/history", tags=["history"])

class ConversationCreate(BaseModel):
	title: str

class ConversationOut(BaseModel):
	id: int
	title: str
	class Config:
		from_attributes = True

class MessageCreate(BaseModel):
	conversation_id: int
	role: str
	content: str

class MessageOut(BaseModel):
	id: int
	role: str
	content: str
	class Config:
		from_attributes = True

@router.post("/conversations", response_model=ConversationOut)
def create_conversation(payload: ConversationCreate, db: Session = Depends(get_db), user_email: str = Depends(get_current_user_email)):
	user = db.execute(select(User).where(User.email == user_email)).scalar_one()
	conv = Conversation(title=payload.title or "Новый диалог", user_id=user.id)
	db.add(conv)
	db.commit()
	db.refresh(conv)
	return conv

@router.get("/conversations", response_model=List[ConversationOut])
def list_conversations(db: Session = Depends(get_db), user_email: str = Depends(get_current_user_email)):
	user = db.execute(select(User).where(User.email == user_email)).scalar_one()
	rows = db.execute(select(Conversation).where(Conversation.user_id == user.id).order_by(Conversation.created_at.desc())).scalars().all()
	return rows

@router.get("/messages/{conversation_id}", response_model=List[MessageOut])
def list_messages(conversation_id: int, db: Session = Depends(get_db), user_email: str = Depends(get_current_user_email)):
	conv = db.get(Conversation, conversation_id)
	if not conv:
		raise HTTPException(404, "Conversation not found")
	rows = db.execute(select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)).scalars().all()
	return rows

@router.post("/messages", response_model=MessageOut)
def add_message(payload: MessageCreate, db: Session = Depends(get_db), user_email: str = Depends(get_current_user_email)):
	conv = db.get(Conversation, payload.conversation_id)
	if not conv:
		raise HTTPException(404, "Conversation not found")
	msg = Message(conversation_id=payload.conversation_id, role=payload.role, content=payload.content)
	db.add(msg)
	db.commit()
	db.refresh(msg)
	return msg
