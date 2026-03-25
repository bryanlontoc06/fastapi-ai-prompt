import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

load_dotenv()
_SECRET_KEY = os.getenv("SECRET_KEY")
_ALGORITHM = os.getenv("ALGORITHM")

if not _SECRET_KEY or not _ALGORITHM:
    raise ValueError("SECRET_KEY or ALGORITHM not found in .env file")

SECRET_KEY: str = _SECRET_KEY
ALGORITHM: str = _ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

security = HTTPBearer(auto_error=False)

def get_user_identifier(res: Annotated[HTTPAuthorizationCredentials | None, Depends(security)]) -> str:
    if res is None:
        print("No token provided, returning global_unauthenticated_user")
        return "global_unauthenticated_user"
    token:str = res.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username