from datetime import timedelta
from typing import Annotated
from src.service import authenticate_user, check_user_access, create_access_token
from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from src.model import Token
import aiofiles
import os

CURRENT_USER = None

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
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
    global CURRENT_USER
    CURRENT_USER = user
    return Token(access_token=access_token, token_type="bearer")


@router.get("/mainPage", response_class=HTMLResponse)
async def main():
    async with aiofiles.open("../webUI/MainPage.html", mode="r") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)


@router.get("/orderListPage", response_class=HTMLResponse)
async def orderListPage():
    if not check_user_access(CURRENT_USER, "/orderListPage"):
        async with aiofiles.open("../webUI/403.html", mode="r") as f:
            html_content = await f.read()
        return HTMLResponse(content=html_content, status_code=403)
        # raise HTTPException(status_code=403, detail="Access Denied")

    async with aiofiles.open("../webUI/orderListPage.html", mode="r") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)


@router.get("/CRMpage", response_class=HTMLResponse)
async def CRMpage():
    if not check_user_access(CURRENT_USER, "/CRMpage"):
        async with aiofiles.open("../webUI/403.html", mode="r") as f:
            html_content = await f.read()
        return HTMLResponse(content=html_content, status_code=403)
        # raise HTTPException(status_code=403, detail="Access Denied!!!!!!!")
    async with aiofiles.open("../webUI/CRMpage.html", mode="r") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)


@router.get("/OMpage", response_class=HTMLResponse)
async def OMpage():
    if not check_user_access(CURRENT_USER, "/OMpage"):
        raise HTTPException(status_code=403, detail="Access Denied")
    async with aiofiles.open("../webUI/OMpage.html", mode="r") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)


@router.get("/LogInPage", response_class=HTMLResponse)
async def LogInPage():
    async with aiofiles.open("../webUI/LogInPage.html", mode="r") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)


@router.get("/SignUpPage", response_class=HTMLResponse)
async def SignUpPage():
    async with aiofiles.open("../webUI/SignUpPage.html", mode="r") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)


@router.get("/bomListPage", response_class=HTMLResponse)
async def bomListPage():
    if not check_user_access(CURRENT_USER, "/bomListPage"):
        async with aiofiles.open("../webUI/403.html", mode="r") as f:
            html_content = await f.read()
        return HTMLResponse(content=html_content, status_code=403)
        # raise HTTPException(status_code=403, detail="Access Denied")
    async with aiofiles.open("../webUI/bomListPage.html", mode="r") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)


@router.get("/componentInventoryPage", response_class=HTMLResponse)
async def componentInventoryPage():
    if not check_user_access(CURRENT_USER, "/componentInventoryPage"):
        async with aiofiles.open("../webUI/403.html", mode="r") as f:
            html_content = await f.read()
        return HTMLResponse(content=html_content, status_code=403)
        # raise HTTPException(status_code=403, detail="Access Denied")
    async with aiofiles.open("../webUI/componentInventoryPage.html", mode="r") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)


@router.get("/customerList", response_class=HTMLResponse)
async def customerList():
    if not check_user_access(CURRENT_USER, "/customerList"):
        async with aiofiles.open("../webUI/403.html", mode="r") as f:
            html_content = await f.read()
        return HTMLResponse(content=html_content, status_code=403)
        # raise HTTPException(status_code=403, detail="Access Denied")
    async with aiofiles.open("../webUI/customerList.html", mode="r") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)


@router.get("/productInventoryPage", response_class=HTMLResponse)
async def productInventoryPage():
    if not check_user_access(CURRENT_USER, "/productInventoryPage"):
        async with aiofiles.open("../webUI/403.html", mode="r") as f:
            html_content = await f.read()
        return HTMLResponse(content=html_content, status_code=403)
        # raise HTTPException(status_code=403, detail="Access Denied")
    async with aiofiles.open("../webUI/productInventoryPage.html", mode="r") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)


@router.get("/rfmCustomerGroupPage", response_class=HTMLResponse)
async def rfmCustomerGroupPage():
    if not check_user_access(CURRENT_USER, "/rfmCustomerGroupPage"):
        async with aiofiles.open("../webUI/403.html", mode="r") as f:
            html_content = await f.read()
        return HTMLResponse(content=html_content, status_code=403)
        # raise HTTPException(status_code=403, detail="Access Denied")
    async with aiofiles.open("../webUI/rfmCustomerGroupPage.html", mode="r") as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)
