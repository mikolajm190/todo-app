from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.api.auth import AuthServiceDep
from src.schemas.todo.create_todo_request import TodoCreateDTO
from src.schemas.todo.todo_response import TodoDTO
from src.schemas.todo.update_todo_request import TodoUpdateDTO
from src.services.auth import AuthTokenDep
from src.services.todo import TodoService

TodoServiceDep = Annotated[TodoService, Depends()]

router = APIRouter()


@router.get("/", responses={401: {"description": "Not authenticated"}})
def read_todos(
    todo_service: TodoServiceDep,
    auth_service: AuthServiceDep,
    token: AuthTokenDep,
    done: Annotated[bool | None, Query()] = None,
    limit: Annotated[int, Query(gt=0)] = 9,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[TodoDTO]:
    auth_service.validate_token(token)
    return todo_service.get_todos(limit, offset, done)


@router.get("/{todo_id}", responses={
    401: {"description": "Not authenticated"},
    404: {"description": "Not found"}
})
def read_todo(
    todo_id: UUID,
    todo_service: TodoServiceDep,
    auth_service: AuthServiceDep,
    token: AuthTokenDep
) -> TodoDTO:
    auth_service.validate_token(token)
    return todo_service.get_todo(todo_id)


@router.post(
    "/",
    status_code=201,
    responses={401: {"description": "Not authenticated"}}
)
def create_todo(
    body: TodoCreateDTO,
    todo_service: TodoServiceDep,
    auth_service: AuthServiceDep,
    token: AuthTokenDep
) -> TodoDTO:
    auth_service.validate_token(token)
    return todo_service.create_todo(body)


@router.put(
    "/{todo_id}",
    responses={
        401: {"description": "Not authenticated"},
        404: {"description": "Not found"}
    }
)
def update_todo(
    todo_id: UUID,
    body: TodoUpdateDTO,
    todo_service: TodoServiceDep,
    auth_service: AuthServiceDep,
    token: AuthTokenDep
) -> TodoDTO:
    auth_service.validate_token(token)
    return todo_service.update_todo(todo_id, body)


@router.delete(
    "/{todo_id}",
    status_code=204,
    responses={404: {"description": "Not found"}}
)
def delete_todo(
    todo_id: UUID,
    todo_service: TodoServiceDep,
    auth_service: AuthServiceDep,
    token: AuthTokenDep
) -> None:
    auth_service.validate_token(token)
    return todo_service.delete_todo(todo_id)
