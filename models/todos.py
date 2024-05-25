from sqlmodel import SQLModel
from pydantic import (
    ValidationError,
    ValidationInfo,
    field_validator,
)


class TodoIn(SQLModel):
    task: str
    completed: bool = False

    # age: int | None = None

    @field_validator('task')
    @classmethod
    def name_must_contain_space(cls, v: str) -> str:
        if ' ' in v:
            raise ValueError('must not contain a space')
        return v.title()


class TodoOut(SQLModel):
    id: int
    task: str
    completed: bool
    # age: int | None = None
