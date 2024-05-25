from typing import Sequence

from entities import TodoEntity
from models import TodoOut


def todo_model_sequence_mapper(todos: Sequence[TodoEntity]) -> Sequence[TodoOut]:
    return [TodoOut(**todo.model_dump()) for todo in todos]


def todo_model_mapper(todo: TodoEntity) -> TodoOut:
    return TodoOut(**todo.model_dump())
