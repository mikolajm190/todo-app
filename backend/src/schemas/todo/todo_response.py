from uuid import UUID

from pydantic import BaseModel


class TodoDTO(BaseModel):
    id: UUID
    title: str
    description: str | None = None
    done: bool
