from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from src.schemas.todo.create_todo_request import TodoCreateDTO
from src.schemas.todo.update_todo_request import TodoUpdateDTO
from src.schemas.todo.todo_response import TodoDTO
from src.db.session import SessionDep
from src.models.todo import Todo

router = APIRouter()


@router.get("/")
def read_todos(
    session: SessionDep,
    skip: int = 0,
    limit: int = 9
    ):
    result = session.execute(select(Todo).order_by(Todo.title).offset(skip).limit(limit)).scalars().all()
    return result


@router.get("/{todo_id}", response_model=TodoDTO)
def read_todo(
    session: SessionDep,
    todo_id: UUID
    ):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="todo not found")
    return todo


@router.post("/", status_code=201, response_model=TodoDTO)
def create_todo(
    session: SessionDep,
    body: TodoCreateDTO
    ):
    todo = Todo(title=body.title, description=body.description)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@router.put("/{todo_id}", response_model=TodoDTO)
def update_todo(
    session: SessionDep,
    todo_id: UUID,
    body: TodoUpdateDTO
    ):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="todo not found")
    todo.title = body.title
    todo.description = body.description
    todo.done = body.done
    session.commit()
    return todo


@router.delete("/{todo_id}", status_code=204)
def delete_todo(
    session: SessionDep,
    todo_id: UUID
    ):
    to_delete_todo = session.get(Todo, todo_id)
    session.delete(to_delete_todo)
    session.commit()