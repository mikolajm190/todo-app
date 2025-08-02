from sqlalchemy import inspect

from src.db.session import SessionLocal, engine
from src.models.base import Base
from src.models.todo import Todo


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
        session.commit()
    print("✅ Test data inserted")