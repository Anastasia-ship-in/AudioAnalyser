from fastapi import FastAPI
from app.routes import router as routes_router
from app.database import Base, engine
from app import models
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(routes_router)


class Settings(BaseModel):
    authjwt_secret_key: str = "your-secret-key"


@AuthJWT.load_config
def get_config():
    return Settings()
