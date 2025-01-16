from datetime import datetime, timedelta, timezone
import os
from src.model import User, UserInDB
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

ROLE_PERMISSIONS = {
    "manager": ["*"],  # 所有頁面
    "headquarter": ["*"],
    "customer": ["/orderListPage"],
    "factory": [
        "/OMpage",
        "/bomListPage",
        "/componentInventoryPage",
        "/productInventoryPage",
    ],
    "supplier": ["/OMpage", "/componentInventoryPage"],
}


fake_users_db = {
    "customer@example.com": {
        "username": "customer@example.com",
        "accountType": "customer",
        "full_name": "John Doe",
        "email": "customer@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "factory@example.com": {
        "username": "factory@example.com",
        "accountType": "factory",
        "full_name": "John Doe",
        "email": "factory@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "manager@example.com": {
        "username": "manager@example.com",
        "accountType": "manager",
        "full_name": "John Doe",
        "email": "manager@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "supplier@example.com": {
        "username": "supplier@example.com",
        "accountType": "supplier",
        "full_name": "John Doe",
        "email": "supplier@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "headquarter@example.com": {
        "username": "headquarter@example.com",
        "accountType": "headquarter",
        "full_name": "John Doe",
        "email": "headquarter@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
}

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(
    schemes=["bcrypt", "argon2", "pbkdf2_sha256", "sha256_crypt"]
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta]):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     logger.debug("run to get_current_user")
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             logger.debug("no username")
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except InvalidTokenError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user


def check_user_access(user: User, page: str = ""):
    if user is not None:
        allowed_pages = ROLE_PERMISSIONS.get(user.accountType, [])
        if "*" in allowed_pages or page in allowed_pages:
            return True
        else:
            return False
    else:
        return False
