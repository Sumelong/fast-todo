from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine, Session


def _get_engine() -> Engine:
    sqlite_file_name = "fast_todo.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    connect_args = {"check_same_thread": False}
    return create_engine(sqlite_url, echo=True, connect_args=connect_args)


DBEngine = _get_engine()


def create_tables(engine: Engine, model: SQLModel) -> None:
    model.metadata.create_all(engine)
