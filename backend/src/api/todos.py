from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends

from src.services.todo import TodoService
from src.schemas.todo.create_todo_request import TodoCreateDTO
from src.schemas.todo.update_todo_request import TodoUpdateDTO
from src.schemas.todo.todo_response import TodoDTO

router = APIRouter()


@router.get("/", response_model=list[TodoDTO])
def read_todos(
    limit: int = 9,
    offset: int = 0,
    service: TodoService = Depends()
    ) -> list[TodoDTO]:
    return [TodoDTO.model_validate(todo) for todo in service.get_todos(limit, offset)]


@router.get(
        "/{todo_id}",
        response_model=TodoDTO,
        responses={404: {"description": "Not found"}}
        )
def read_todo(
    todo_id: UUID,
    service: TodoService = Depends()
    ) -> TodoDTO:
    return TodoDTO.model_validate(service.get_todo(todo_id))


@router.post("/", status_code=201, response_model=TodoDTO)
def create_todo(
    body: TodoCreateDTO,
    service: TodoService = Depends()
    ) -> TodoDTO:
    return TodoDTO.model_validate(service.create_todo(body))


@router.put(
        "/{todo_id}",
        response_model=TodoDTO,
        responses={404: {"description": "Not found"}}
        )
def update_todo(
    todo_id: UUID,
    body: TodoUpdateDTO,
    service: TodoService = Depends()
    ) -> TodoDTO:
    return TodoDTO.model_validate(service.update_todo(todo_id, body))


@router.delete(
        "/{todo_id}",
        status_code=204,
        responses={404: {"description": "Not found"}}
        )
def delete_todo(
    todo_id: UUID,
    service: TodoService = Depends()
    ):
    return service.delete_todo(todo_id)