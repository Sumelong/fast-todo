from typing import Annotated, Sequence, Type
from fastapi import APIRouter, HTTPException, Path, Request
from starlette.responses import JSONResponse, HTMLResponse

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from entities import TodoEntity
from models import TodoIn, TodoOut
from services import Flash
from usecases import (
    todos_getter,
    todo_getter,
    todo_adder,
    todo_updater,
    todo_deleter
)

TodoWebRouter = APIRouter(
    prefix="/todos",
    responses={404: {"description": "Not found"}},
)

TodoWebRouter.mount("/static", StaticFiles(directory="presentation/web/static"), name="static")
templates = Jinja2Templates(directory="presentation/web/templates")


@TodoWebRouter.get("/",  response_class=HTMLResponse)
async def home(skip: int = 0, limit: int = 10) -> HTMLResponse:
    todos = todos_getter(limit, skip)
    flash = Flash("Todos", "success")
    return templates.TemplateResponse(
        name="views/home.html.jinja",
        context={
            "todos": todos,
            "flash": flash,
        },

        status_code=200,
    )


@TodoWebRouter.get("/{todo_id}/", response_model=TodoOut)
async def get_todo(todo_id: int) -> TodoOut:
    todo = todo_getter(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Not Found")
    return todo


@TodoWebRouter.post("/todo/", response_model=TodoOut)
async def create_todo(todo: TodoIn):
    new_todo = todo_adder(todo)
    if new_todo == 0:
        raise HTTPException(status_code=500, detail="validation failed")
    elif new_todo == 1:
        raise HTTPException(status_code=409, detail="task already present")
    else:
        return new_todo


@TodoWebRouter.put("/{todo_id}/", response_model=TodoOut, responses={403: {"description": "Operation forbidden"}}, )
async def update_todo(
        todo_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
        q: str | None = None, todo: TodoIn | None = None, ) -> int | TodoEntity:
    new_todo = todo_updater(todo_id, todo)
    if new_todo == 0:
        raise HTTPException(status_code=404, detail="Todo not found in list")
    return new_todo


@TodoWebRouter.delete("/{todo_id}/")
async def remove_todo(
        todo_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)]) \
        -> JSONResponse:
    todo = todo_deleter(todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(status_code=404, content={"message": "Item removed"})
