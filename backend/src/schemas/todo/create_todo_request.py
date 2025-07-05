from pydantic import BaseModel


class TodoCreateDTO(BaseModel):
    title: str
    description: str | None = None