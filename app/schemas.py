from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    name: str
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class AIRequestCreate(BaseModel):
    user_id: int
    endpoint_type: str
    input_text: str


class AIHistoryResponse(BaseModel):
    request_id: int
    user_id: int
    endpoint_type: str
    input_text: str
    output_text: Optional[str]
    created_at: datetime


class AIProcessRequest(BaseModel):
    user_id: int
    input: str


class AIProcessResponse(BaseModel):
    result: str
    request_id: int