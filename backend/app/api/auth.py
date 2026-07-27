from fastapi import APIRouter
from pydantic import BaseModel

from app.services.auth_service import AuthService

router = APIRouter()


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
async def register(request: RegisterRequest):

    return AuthService.register(
        request.username,
        request.email,
        request.password
    )


@router.post("/login")
async def login(request: LoginRequest):

    return AuthService.login(
        request.email,
        request.password
    )