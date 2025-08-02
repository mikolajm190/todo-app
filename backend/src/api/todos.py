from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.schemas.todo.create_todo_request import TodoCreateDTO
from src.schemas.todo.todo_response import TodoDTO
from src.schemas.todo.update_todo_request import TodoUpdateDTO
from src.services.todo import TodoService

router = APIRouter()


@router.get("/")
def read_todos(
    limit: Annotated[int, Query(gt=0)] = 9,
    offset: Annotated[int, Query(ge=0)] = 0,
    done: bool | None = None,
    service: TodoService = Depends(),
) -> list[TodoDTO]:
    return service.get_todos(limit, offset, done)


@router.get("/{todo_id}", responses={404: {"description": "Not found"}})
def read_todo(todo_id: UUID, service: TodoService = Depends()) -> TodoDTO:
    return service.get_todo(todo_id)


@router.post("/", status_code=201)
def create_todo(body: TodoCreateDTO, service: TodoService = Depends()) -> TodoDTO:
    return service.create_todo(body)


@router.put("/{todo_id}", responses={404: {"description": "Not found"}})
def update_todo(
    todo_id: UUID, body: TodoUpdateDTO, service: TodoService = Depends()
) -> TodoDTO:
    return service.update_todo(todo_id, body)


@router.delete(
    "/{todo_id}", status_code=204, responses={404: {"description": "Not found"}}
)
def delete_todo(todo_id: UUID, service: TodoService = Depends()) -> None:
    return service.delete_todo(todo_id)
