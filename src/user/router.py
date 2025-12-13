from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import re

from database import get_async_session
from templates import render_template
from user.schemas import UserCreateSchema, UserReadSchema

from .repository import Repository
from .utils import make_token, check

router = APIRouter(tags=["users"], prefix="/users")
get_token = OAuth2PasswordBearer(tokenUrl="/users/login")

# регистрация пользователя
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    request: Request,
    login: str = Form(),
    email: str = Form(),
    password: str = Form(),
    password_repeat=Form(),
    session: AsyncSession = Depends(get_async_session),
    repository: Repository = Depends(),
):
    
    if login.strip() == "" or password.strip() == "" or password_repeat.strip() == "":
        return render_template(
            "register.html",
            request=request,
            message="Необходимо заполнить поля логина и пароля!",
        )
    
    if len(login) < 3 or len(password) < 3:
        return render_template(
            "register.html",
            request=request,
            message="Слишком короткий логин или пароль",
        )
    
    if not check(email):
        return render_template(
            "register.html",
            request=request,
            message="Проверьте правильность ввода email",
        )


    
    if password == password_repeat:
        user = UserCreateSchema(nickname=login, email=email, password=password, data="")
        try:
            result = await repository.create_user(user, session)
            return render_template(
                "registration_success.html", request=request, username=result.nickname
            )

        except HTTPException as e:
            return render_template(
                "register.html",
                request=request,
                message="такой пользователь существует, пройдите авторизацию повторно! <br />" + e.detail,
            )
    else:
        return render_template("register.html", request=request, message="Пароли не равны")

# вывод всех пользователей
@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(
    repository: Repository = Depends(), session=Depends(get_async_session)
) -> list[UserReadSchema]:
    return await repository.get_users(session)

# авторизация пользователя
@router.post("/login")
async def login_user(
    request: Request,
    response: Response,
    login: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(get_async_session),
    repository_user: Repository = Depends(),
):
    if login.strip() == "" or password.strip() == "":
        return render_template(
            "login.html",
            request=request,
            message="Необходимо заполнить поля логина и пароля!",
        )
    if len(login) < 3 or len(password) < 3:
        return render_template(
            "login.html",
            request=request,
            message="Слишком короткий логин или пароль",
        )
    try:
        result = await repository_user.get_user(login, password, session)
        return render_template(
            "user_page.html", request=request, response=response, username=result.nickname,
        )
    except HTTPException as e:
        return render_template(
            "login.html",
            request=request,
            message=f"{e.detail}! Попробуйте еще раз"
        )

# верификация регистрации через email
@router.get("/verify")
async def users_verify(random_string: str, request: Request, session: AsyncSession = Depends(get_async_session),
                       repository: Repository = Depends()):
    username = await repository.verify_user(random_string, session)
    return render_template("user_page.html", username=username, request=request )

@router.post("/password_update")
async def password_update(request: Request, password: str = Form(), password_repeat: str = Form(), 
                          random_string: str = Form(), 
                          session=Depends(get_async_session),
                          repository: Repository = Depends()):
    user_password_update = await repository.password_update(nickname, user, session)
    return user_password_update


