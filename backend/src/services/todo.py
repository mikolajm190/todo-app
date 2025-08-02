from uuid import UUID

from fastapi import Depends, HTTPException, status

from src.models.todo import Todo
from src.repositories.todo import TodoDAO
from src.schemas.todo.create_todo_request import TodoCreateDTO
from src.schemas.todo.update_todo_request import TodoUpdateDTO
from src.schemas.todo.todo_response import TodoDTO


class TodoService:
    """Class for implementing business logic of todos."""

    def __init__(self, dao: TodoDAO = Depends()) -> None:
        self.dao = dao

    def get_todos(self, limit: int, offset: int, done: bool | None) -> list[TodoDTO]:
        return [TodoDTO.model_validate(todo)
                for todo in self.dao.get_all(limit, offset, done)]
    
    def get_todo(self, todo_id: UUID) -> TodoDTO:
        todo = self.dao.get_by_id(todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )
        return TodoDTO.model_validate(todo)
    
    def create_todo(self, body: TodoCreateDTO) -> TodoDTO:
        return TodoDTO.model_validate(self.dao.create(**body.model_dump()))
        
    def update_todo(self, todo_id: UUID, body: TodoUpdateDTO) -> TodoDTO:
        todo = self.dao.update(todo_id, **body.model_dump())
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )
        return TodoDTO.model_validate(todo)
    
    def delete_todo(self, todo_id: UUID) -> None:
        is_deleted = self.dao.delete(todo_id)
        if not is_deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found"
            )