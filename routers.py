from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Path
from database import get_engine
from model import TodoPublic, TodoCreate, Todo

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    dependencies=[Depends(get_engine)],
    responses={404: {"description": "Not found"}},
)

todo_list = [
    Todo(id=1, task="Todo 1", completed=False),
    Todo(id=2, task="Todo 2", completed=False),
    Todo(id=3, task="Todo 3", completed=False),
    Todo(id=4, task="Todo 4", completed=False),
    Todo(id=5, task="Todo 5", completed=False),
]


@router.get("/", response_model=list[TodoPublic])
async def home() -> list[Todo]:
    return todo_list


@router.get("/{todo_id}/", response_model=TodoPublic)
async def get_todo(todo_id: int):
    return todo_list[todo_id - 1]


@router.post(
    "/todo/",
    response_model=TodoPublic)
async def create_todo(todo: TodoCreate):
    for item in todo_list:
        if item.task == todo.task:
            raise HTTPException(
                status_code=409,
                detail="todo already present in the list"
            )
        new_todo = Todo(task=todo.task, completed=todo.completed)
        todo_list.append(new_todo)
    return todo_list


@router.put(
    "/{todo_id}/",
    response_model=TodoPublic,
    responses={403: {"description": "Operation forbidden"}}, )
async def update_todo(
        todo_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
        q: str | None = None,
        todo: TodoCreate | None = None, ) -> list[Todo]:
    for item in todo_list:
        if item.id == todo_id:
            data_todo = Todo(id=5, task=todo.task, completed=todo.completed)
            todo_list.append(data_todo)
            return todo_list
        raise HTTPException(
            status_code=403, detail="Todo not found in list"
        )


@router.delete(
    "/{todo_id}/",
    response_model=TodoPublic,
    responses={403: {"description": "Operation forbidden"}}, )
async def remove_todo(todo_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)]) -> list[Todo]:
    for item in todo_list:
        if item.id == todo_id:
            data_todo = Todo(id=item.id, task=item.task, completed=item.completed)
            todo_list.remove(data_todo)
            return todo_list
        raise HTTPException(
            status_code=403, detail="Todo not found in list"
        )
