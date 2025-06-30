from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from src.api import todos
from src.db.session import engine
from src.db.init_db import create_tables, insert_test_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_tables()
    except Exception as e:
        print("Failed to create tables", e)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(todos.router, prefix="/api/v1/todos", tags=["Todos"])

@app.get("/", status_code=200)
def get_root():
    return {"status": "UP"}

@app.get("/db", status_code=200)
def test_connection():
    try:
        with engine.connect() as conn:
            return {"status": conn.scalar(text("SELECT 'UP';"))}
    except Exception as e:
        print("DB connection failed:", e)