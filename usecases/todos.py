from typing import Any, Sequence

from pydantic import ValidationError
from mappers import todo_model_sequence_mapper
from models import TodoIn, TodoOut
from entities import (
    TodoEntity, create_todo, read_todo,
    read_todos, update_todo, delete_todo)


def todo_adder(new_todo: TodoIn) -> int | TodoOut:
    try:
        entity_todo = TodoEntity(**new_todo.model_dump(exclude_unset=True))
    except ValidationError as e:
        return 0

    todo = create_todo(entity_todo)
    if todo == 1:
        return 1
    model_todo = TodoOut(**todo.model_dump())
    return model_todo


def todos_getter(limit: int, offset: int) -> Sequence[TodoOut]:
    entity_todos = read_todos(limit, offset)
    return todo_model_sequence_mapper(entity_todos)


def todo_getter(todo_id: int) -> TodoOut | None:
    todo = read_todo(todo_id)
    if todo is None:
        return None
    return TodoOut(**todo.model_dump())


def todo_updater(todo_id: int, todo: TodoIn) -> int | TodoEntity:
    entity_todo = TodoEntity(**todo.model_dump(exclude_unset=True))
    updated_todo = update_todo(todo_id, entity_todo)
    if updated_todo is None:
        return 0
    return updated_todo


def todo_deleter(todo_id: int) -> int | None:
    result = delete_todo(todo_id)
    if result is None:
        return None
    return 1
