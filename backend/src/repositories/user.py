from sqlalchemy import select

from src.db.session import SessionDep
from src.models.user import User


class UserDAO:
    """Class for accessing the user table."""

    def __init__(self, session: SessionDep) -> None:
        self.session = session

    def get_by_username(self, username: str) -> User | None:
        query = (
            select(User)
            .where(User.username == username)
            .limit(1)
        )
        user = self.session.execute(query)
        return user.scalar()