from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine


def get_engine() -> Engine:
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    connect_args = {"check_same_thread": False}
    return create_engine(sqlite_url, echo=True, connect_args=connect_args)


def get_model() -> SQLModel:
    return SQLModel()


def create_tables(engine: Engine, model: SQLModel) -> None:
    model.metadata.create_all(engine)
