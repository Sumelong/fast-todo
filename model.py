from database import get_model as model
from sqlmodel import Field, SQLModel


class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    task: str = Field(index=True)
    completed: bool
    secrets: str = "my secrete"
    # age: int | None = Field(default=None, index=True)


class TodoCreate(SQLModel):
    task: str
    completed: bool
    # age: int | None = None


class TodoPublic(SQLModel):
    id: int
    task: str
    completed: bool
    # age: int | None = None
