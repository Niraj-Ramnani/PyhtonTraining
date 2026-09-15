from fastapi import HTTPException , status , Request , Depends
from sqlalchemy.orm import Session
from src.user.models import UserModel 
import jwt
from jwt.exceptions import InvalidTokenError
from src.utils.settings import settings
from src.utils.db import get_db



def is_authenticated(request: Request, db: Session = Depends(get_db)):

    token = request.headers.get("Authorization")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized"
        )

    token = token.split(" ")[-1]

    try:
        data = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user_id = data.get("_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = db.get(UserModel, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user