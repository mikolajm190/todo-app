from uuid import UUID

from sqlalchemy import select

from src.db.session import SessionDep
from src.models.todo import Todo


class TodoDAO:
    """Class for accessing the todo table."""

    def __init__(self, session: SessionDep) -> None:
        self.session = session

    def get_by_id(self, todo_id: UUID) -> Todo | None:
        return self.session.get(Todo, todo_id)
    
    def get_all(self, limit: int, offset: int) -> list[Todo]:
        todos = self.session.execute(select(Todo).order_by(Todo.title).limit(limit).offset(offset))
        return list(todos.scalars().all())
    
    def create(self, title: str, description: str | None) -> Todo:
        todo = Todo(title=title, description=description)
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo
    
    def update(self, todo_id: UUID, title: str, description: str | None, done: bool) -> Todo | None:
        todo = self.session.get(Todo, todo_id)
        if todo:
            todo.title = title
            todo.description = description
            todo.done = done
        self.session.commit()
        return todo
    
    def delete(self, todo_id: UUID) -> bool:
        todo = self.session.get(Todo, todo_id)
        if todo is None:
            return False
        self.session.delete(todo)
        self.session.commit()
        return True
