from typing import Annotated, Sequence, Type
from fastapi import APIRouter, HTTPException, Path
from starlette.responses import JSONResponse

from entities import TodoEntity
from models import TodoIn, TodoOut
from usecases import (
    todos_getter,
    todo_getter,
    todo_adder,
    todo_updater,
    todo_deleter
)

TodoApiRouter = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)


@TodoApiRouter.get("/", response_model=Sequence[TodoOut])
async def home(skip: int = 0, limit: int = 10) -> Sequence[TodoOut]:
    return todos_getter(limit, skip)


@TodoApiRouter.get("/{todo_id}/", response_model=TodoOut)
async def get_todo(todo_id: int) -> TodoOut:
    todo = todo_getter(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return todo


@TodoApiRouter.post("/todo/", response_model=TodoOut)
async def create_todo(todo: TodoIn):
    new_todo = todo_adder(todo)
    if new_todo == 0:
        raise HTTPException(status_code=500, detail="validation failed")
    elif new_todo == 1:
        raise HTTPException(status_code=409, detail="task already present")
    else:
        return new_todo


@TodoApiRouter.put("/{todo_id}/", response_model=TodoOut, responses={403: {"description": "Operation forbidden"}}, )
async def update_todo(
        todo_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
        q: str | None = None, todo: TodoIn | None = None, ) -> int | TodoEntity:
    new_todo = todo_updater(todo_id, todo)
    if new_todo == 0:
        raise HTTPException(status_code=404, detail="Todo not found in list")
    return new_todo


@TodoApiRouter.delete("/{todo_id}/")
async def remove_todo(
        todo_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)]) \
        -> JSONResponse:
    todo = todo_deleter(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(status_code=404, content={"message": "Item removed"})
