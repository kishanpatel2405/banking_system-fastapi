from fastapi import Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.models import User
from app.database import get_db
from sqlalchemy.orm import Session
from app.security import verify_token  # Make sure to import from the correct module

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = verify_token(token)  # Ensure verify_token is imported from security.py
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
