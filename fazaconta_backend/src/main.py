from http import HTTPStatus
from time import sleep
from typing import Annotated
import uuid

from fastapi import Depends, FastAPI, Request
from application import create_app
from commands import CreateTodo
from queries import GetAllTodos
from lato import Application
import uvicorn

api = FastAPI()
api.lato_application = create_app()


def get_application(request: Request) -> Application:
    """
    Retrieve the application instance from the request.

    :param request: The incoming request.
    :return: The Application instance.
    """

    app = request.app.lato_application
    return app


@api.get("/todo")
def root(app: Annotated[Application, Depends(get_application)]):
    result = app.execute(GetAllTodos())
    return {"todos": result}


@api.post("/todo", status_code=HTTPStatus.CREATED)
def root(todo: CreateTodo, app: Annotated[Application, Depends(get_application)]):
    result = app.execute(
        CreateTodo(
            id=todo.todo_id,
            title=todo.title,
            description=todo.description,
            due_at=todo.due_at,
        )
    )

    return {"todo": result}


if __name__ == "__main__":
    uvicorn.run("main:api", host="0.0.0.0", port=8000, reload=True)
