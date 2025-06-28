from fastapi import FastAPI
from sqlalchemy import text

from api import todos
from db.session import engine

app = FastAPI()
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