from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langflow.services.auth import create_user

router = APIRouter(tags=["Authentication"])

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

@router.post("/register")
async def register(user: UserCreate):
    try:
        new_user = await create_user(
            username=user.username,
            password=user.password,
            email=user.email
        )
        return {"message": "User created successfully", "username": new_user.username}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )