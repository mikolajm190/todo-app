from typing import Annotated

from pydantic import BaseModel, Field


class TodoUpdateDTO(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=50)]
    description: Annotated[str | None, Field(max_length=200, default=None)]
    done: bool
