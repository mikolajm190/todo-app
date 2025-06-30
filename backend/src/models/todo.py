from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from src.models.base import Base

class Todo(Base):
    '''Class representing a todo'''

    __tablename__ = "todos"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
        )
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200))
    done: Mapped[bool] = mapped_column(nullable=False, default=False)
