from fastapi import HTTPException , status , Request
from src.user.dtos import UserSchema , LoginSchmea
from sqlalchemy.orm import Session
from src.user.models import UserModel 
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from src.utils.settings import settings
from datetime import datetime , timedelta

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)

def register(body:UserSchema , db:Session):
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(400,detail="username already exisist")
    is_user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user:
        raise HTTPException(400,detail="Email already exisist")
    hashed_password = get_password_hash(body.password)

    new_user = UserModel(
        name = body.name,
        username = body.username,
        hash_password = hashed_password,
        email = body.email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(body:LoginSchmea , db : Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="You entered wrong password ")
    if not verify_password(body.password , user.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="You entered wrong password ")
    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME)
    token = jwt.encode({"_id" : user.id , "username" : user.username , "exp" : exp_time.timestamp()},settings.SECRET_KEY,settings.ALGORITHM)
    return {"token" : token}


def is_authenticated(request: Request, db: Session):

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