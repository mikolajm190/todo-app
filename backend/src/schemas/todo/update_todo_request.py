from pydantic import BaseModel


class TodoUpdateDTO(BaseModel):
    title: str
    description: str | None = None
    done: bool