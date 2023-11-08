from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()
metadata_obj = Base.metadata


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    assignee_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
