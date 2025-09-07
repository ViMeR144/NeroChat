from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	email = Column(String(255), unique=True, index=True, nullable=False)
	password_hash = Column(String(255), nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)
	conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")

class Conversation(Base):
	__tablename__ = "conversations"
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String(255), nullable=False, default="Новый диалог")
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)
	user = relationship("User", back_populates="conversations")
	messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
	__tablename__ = "messages"
	id = Column(Integer, primary_key=True, index=True)
	conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
	role = Column(String(32), nullable=False)
	content = Column(Text, nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)
	conversation = relationship("Conversation", back_populates="messages")
