from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    accountType: str
    email: Optional[str]
    full_name: Optional[str]
    disabled: Optional[bool]


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str]


class SignUpRequest(BaseModel):
    passID: str
    emailAddress: str
    setPassword: str
    checkPassword: str
