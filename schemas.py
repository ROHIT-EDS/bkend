from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class MessageIn(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[MessageIn]
