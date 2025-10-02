import hashlib
from random import choices
from string import ascii_letters

from .schemas import UserCreateSchema, UserReadSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert,delete, update
from fastapi import HTTPException, status
from .models import User



class Repository:

    def get_hash(self, password: str, salt: str) -> str:
        password_hash = hashlib.sha256(password.encode() + salt.encode()).hexdigest()
        return password_hash

    async def create_user(self, user: UserCreateSchema, session: AsyncSession) -> UserCreateSchema:
        statement = select(User).where(User.nickname == user.nickname)
        result = await session.scalar(statement)
        if result is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Такой пользователь уже есть")
        salt = "".join(choices(ascii_letters, k=16))
        password_hash = self.get_hash(user.password, salt)
        statement = insert(User).values(
            nickname=user.nickname,
            data=user.data,
            password_hash=password_hash,
            password_salt=salt,
        ).returning(User)
        result = await session.scalar(statement)
        await session.commit()
        return result

    async def get_users(self, session: AsyncSession) -> list[UserReadSchema]:
        statement = select(User)
        result = await session.scalars(statement)
        return result

    async def get_user(self, nickname: str, password: str, session: AsyncSession) -> UserReadSchema:
        statement = select(User).where(User.nickname == nickname)
        result = await session.scalar(statement)
        if result is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")
        password_hash = self.get_hash(password, result.password_salt)
        if result.password_hash == password_hash:
            return result
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль")
        

