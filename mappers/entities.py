from entities import TodoEntity
from models import TodoOut


def todo_entity_mapper(todo: TodoOut) -> TodoEntity:
    return TodoEntity(**todo.model_dump(exclude_unset=True))
