from fastapi import FastAPI
from user.router import router as user_router
from view import router as view_router

app = FastAPI()
app.include_router(user_router)
app.include_router(view_router)

