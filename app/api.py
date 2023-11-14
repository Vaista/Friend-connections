from fastapi import FastAPI

from app.routes.user import user_router
from app.routes.add_friends import add_friend_router


app = FastAPI()


app.include_router(user_router)
app.include_router(add_friend_router)
