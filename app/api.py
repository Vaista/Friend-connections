from fastapi import FastAPI, HTTPException
from neomodel import db
from fastapi.middleware.cors import CORSMiddleware

from app.routes.user import user_router


app = FastAPI()


app.include_router(user_router)
