"""Esquemas Pydantic para validar entradas y salidas."""

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    full_name: str = Field(min_length=2)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class OTPVerify(BaseModel):
    email: EmailStr
    code: str = Field(min_length=6, max_length=6)


class OTPResend(BaseModel):
    email: EmailStr


class UserUpdate(BaseModel):
    full_name: str = Field(min_length=2)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class Message(BaseModel):
    message: str
