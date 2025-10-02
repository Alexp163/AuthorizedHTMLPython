from fastapi import APIRouter, Depends, status
from fastapi import Request
from database import get_async_session
from templates import render_template 
from user.schemas import UserCreateSchema
from user.repository import Repository 
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession 


router = APIRouter(tags=["index"])

@router.get("/")
async def index(request: Request, session=Depends(get_async_session)):
    return render_template("index.html", request=request)


@router.get("/register", status_code=status.HTTP_201_CREATED)
async def register(request: Request, session=Depends(get_async_session)):
    return render_template("register.html", request=request, session=session)


@router.get("/login", status_code=status.HTTP_200_OK)
async def login(request: Request, session=Depends(get_async_session)):
    return render_template("login.html", request=request, session=session)

@router.get("/user_page", status_code=status.HTTP_200_OK)
async def user_page(request: Request, session=Depends(get_async_session)):
    return render_template("user_page.html", request=request, session=session)


