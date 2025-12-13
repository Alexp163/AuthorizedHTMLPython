import hashlib
import os
import smtplib
from random import choices
from dotenv import load_dotenv
from string import ascii_letters

from fastapi import HTTPException, status
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .schemas import UserCreateSchema, UserReadSchema, UserUpdateSchema
from .utils import email_sending


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



class Repository:
    def get_hash(self, password: str, salt: str) -> str:
        password_hash = hashlib.sha256(password.encode() + salt.encode()).hexdigest()
        return password_hash

    # создание user
    async def create_user(self, user: UserCreateSchema, session: AsyncSession) -> UserReadSchema:
        statement_email = select(User).where(User.email == user.email)
        result_email = await session.scalar(statement_email)
        if result_email is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Пользователь с такой почтой уже есть"
            )
        statement = select(User).where(User.nickname == user.nickname)
        result = await session.scalar(statement)
        if result is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Такой пользователь уже есть"
            )
        salt = "".join(choices(ascii_letters, k=16))
        random_string = "".join(choices(ascii_letters, k=16))
        password_hash = self.get_hash(user.password, salt)
        statement = (
            insert(User)
            .values(
                nickname=user.nickname,
                data=user.data,
                email=user.email,
                random_string=random_string, 
                password_hash=password_hash,
                password_salt=salt,
            )
            .returning(User)
        )
        result = await session.scalar(statement)
        await session.commit()
        email_sending(user.email, f"Добрый день, {user.nickname} Верифицируйтесь,"
                      f"пожалуйста! http://127.0.0.1:8004/users/verify?random_string={random_string}", "Верификация пользователя!")
        return result

    # вывести всех users
    async def get_users(self, session: AsyncSession) -> list[UserReadSchema]:
        statement = select(User)
        result = await session.scalars(statement)
        return result

    # получить user
    async def get_user(self, nickname: str, password: str, session: AsyncSession) -> UserReadSchema:
        statement = select(User).where(User.nickname == nickname)
        result = await session.scalar(statement)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль"
            )
        password_hash = self.get_hash(password, result.password_salt)

        if result.password_hash != password_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль"
            )
        if result.email_verified == False:
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Вы не подтвердили электронную почту"
            )
        return result
    
    # верификация user через электронную почту
    async def verify_user(self, random_string: str, session: AsyncSession) -> None:
        statement = select(User).where(User.random_string == random_string)
        result = await session.scalar(statement)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Такой пользователь не найден"
            )
        update_random_string = "".join(choices(ascii_letters, k=16)) # обновление random_string
        statement = update(User).where(User.random_string == random_string).values(
            email_verified=True, random_string=update_random_string,
        )
        await session.execute(statement)
        await session.commit()
        return result.nickname
    
    async def password_update(self, nickname: str, user: UserUpdateSchema, 
                              session: AsyncSession) -> UserReadSchema:
        statement = select(User).where(User.nickname == nickname)
        result = await session.scalar(statement)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Такого пользователя не существует")
        if result.nickname == nickname:
            salt = "".join(choices(ascii_letters, k=16))
            password_hash = self.get_hash(user.password, salt)
            statement = update(User).where(User.nickname == nickname).values(
                password_hash=password_hash,
                password_salt=salt,
            ).returning(User)
            result = await session.scalar(statement)
            await session.commit()
            return result 
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Отказано в доступе")
        
    




        

        

