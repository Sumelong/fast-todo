from typing import Sequence

from sqlalchemy import String
from sqlmodel import Field, NVARCHAR, Session, select
from configs import EntityBase, DBEngine


class TodoEntity(EntityBase, table=True):
    __tablename__ = "todos"

    id: int | None = Field(default=None, primary_key=True)
    task: str = NVARCHAR(50)
    completed: bool
    secrets: str | None = Field(default=None, max_length=50)
    # age: int | None = Field(default=None, index=True)


def create_todo(todo: TodoEntity) -> int | TodoEntity:
    with Session(DBEngine) as session:
        # check if task already exist and return 1
        stmt = select(TodoEntity).where(TodoEntity.task == todo.task)
        exist_todo = session.exec(stmt).one_or_none()
        if exist_todo:
            return 1
        # if task not exist return new created
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo


def read_todos(limit: int, offset: int) -> Sequence[TodoEntity]:
    with Session(DBEngine) as session:
        stmt = select(TodoEntity).limit(limit).offset(offset)
        return session.exec(stmt).all()


def read_todo(todo_id: int) -> TodoEntity | None:
    with Session(DBEngine) as session:
        stmt = select(TodoEntity).where(TodoEntity.id == todo_id)
        todo = session.exec(stmt).one_or_none()
        if todo:
            return todo
        return None


def update_todo(todo_id: int, todo: TodoEntity) -> TodoEntity | None:
    with Session(DBEngine) as session:
        # check if task exist
        stmt = select(TodoEntity).where(TodoEntity.id == todo_id)
        db_todo = session.exec(stmt).one_or_none()
        if not db_todo:
            return None
        # if not existing update and save

        db_todo.task = todo.task
        db_todo.completed = todo.completed

        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo


def delete_todo(todo_id: int) -> int | None:
    with Session(DBEngine) as session:
        # check if exist
        stmt = select(TodoEntity).where(TodoEntity.id == todo_id)
        exist_todo = session.exec(stmt).one_or_none()
        if exist_todo is None:
            return None
        # remove the task
        session.delete(exist_todo)
        session.commit()
        return 0


