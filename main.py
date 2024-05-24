from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import create_tables, get_engine, get_model
from routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    model = get_model()
    create_tables(engine, model)
    yield
    engine.dispose()


app = FastAPI()
app.include_router(router)


