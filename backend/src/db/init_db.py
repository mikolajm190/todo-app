import os

from sqlalchemy import inspect

from src.db.session import SessionLocal, engine
from src.models.base import Base
from src.models.todo import Todo
from src.models.user import User

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


def create_tables():
    Base.metadata.create_all(engine)
    tables = inspect(engine).get_table_names()
    print(f"✅ Tables created: {tables}")


def insert_test_data():
    print("🧪 Inserting test data...")
    with SessionLocal() as session:

        session.add_all([
            Todo(title=f"Todo {i}", description=f"desc {i}")
            for i in range(1, 13)
            ])
        session.add(User(
            username=ADMIN_USERNAME,
            password=ADMIN_PASSWORD
        ))
        session.commit()
    print("✅ Test data inserted")