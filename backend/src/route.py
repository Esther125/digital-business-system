from datetime import timedelta
import os
import aiofiles
from typing import Annotated
from src.service import authenticate_user, check_user_access, create_access_token
from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from src.model import Token


fake_users_db = {
    "johndoe@example.com": {
        "username": "johndoe@example.com",
        "accountType": "customer",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
}

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# @router.get("/users/me")
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return current_user


@router.get("/mainPage", response_class=HTMLResponse)
async def main():
    async with aiofiles.open("../webUI/MainPage.html", mode="r") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)


@router.get("/orderListPage", response_class=HTMLResponse)
async def orderListPage(
    access: bool = Depends(lambda: check_user_access(page="/orderListPage")),
):
    async with aiofiles.open("../webUI/orderListPage.html", mode="r") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)


@router.get("/CRMpage", response_class=HTMLResponse)
async def CRMpage():
    async with aiofiles.open("../webUI/CRMpage.html", mode="r") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)


@router.get("/OMpage", response_class=HTMLResponse)
async def OMpage():
    async with aiofiles.open("../webUI/OMpage.html", mode="r") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)


@router.get("/LogInPage", response_class=HTMLResponse)
async def LogInPage():
    async with aiofiles.open("../webUI/LogInPage.html", mode="r") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)
