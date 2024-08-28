from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models import User

router = APIRouter()

@router.get("/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
