from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TodoDTO(BaseModel):
    id: UUID
    title: str
    description: str | None
    done: bool

    model_config = ConfigDict(from_attributes=True)
