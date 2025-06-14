from fastapi import FastAPI

app = FastAPI()

@app.get("/", status_code=200)
def get_root():
    return {"status": "ready"}

""" import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

def main():
    load_dotenv()

    DATABASE_URL = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['POSTGRES_DB']}"
    engine = create_engine(DATABASE_URL, echo=True)

    with engine.connect() as connection:
        result = connection.execute(text("select 'hello world'"))
        print(result.all())

if __name__ == "__main__":
    main()
 """