import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from src.models.user import User
from src.repositories.user import UserDAO
from src.schemas.auth.token_response import TokenResponseDTO

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "")
ALGORITHM = os.getenv("HASHING_ALGORITHM", "")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRATION", 0))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

PasswordFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
AuthTokenDep = Annotated[str, Depends(oauth2_scheme)]

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)


class AuthService:
    """Class for implementing authentication logic."""

    def __init__(self, dao: UserDAO = Depends()) -> None:
        self.dao = dao
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_user(self, username: str) -> User | None:
        return self.dao.get_by_username(username)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def authenticate_user(self, username: str, password: str) -> User | None:
        user = self.get_user(username)
        if not user:
            return None
        if not self.verify_password(password, user.password):
            return None
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def get_access_token(self, form_data: PasswordFormDep) -> TokenResponseDTO:
        user = self.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"}
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return TokenResponseDTO(access_token=access_token, token_type="bearer")
    
    def validate_token(self, token: AuthTokenDep) -> None:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
        except InvalidTokenError:
            raise credentials_exception
        user = self.dao.get_by_username(username)
        if user is None:
            raise credentials_exception
