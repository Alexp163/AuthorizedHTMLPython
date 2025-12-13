from fastapi import APIRouter, Depends, Request, status

from database import get_async_session
from templates import render_template

router = APIRouter(tags=["index"])


@router.get("/")
async def index(request: Request):
    return render_template("index.html")


@router.get("/register", status_code=status.HTTP_201_CREATED)
async def register(request: Request):
    return render_template("register.html", request=request)


@router.get("/login", status_code=status.HTTP_200_OK)
async def login(request: Request):
    return render_template("login.html", request=request)


@router.get("/user_page", status_code=status.HTTP_200_OK)
async def user_page(request: Request):
    return render_template("user_page.html", request=request)


@router.get("/password_update")
async def password_update(request: Request):
    return render_template("password_update.html", request=request)


@router.get("/password_reset")
async def password_reset(random_string: str, request: Request):
    return render_template("password_reset.html", request=request, random_string=random_string)

