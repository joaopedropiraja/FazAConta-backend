from fastapi import Depends, FastAPI
from http import HTTPStatus
from typing import Annotated

from config.lato_app import get_lato_app, set_lato_app
from lato import Application
import uvicorn

api = FastAPI()

# Cria uma aplicação da biblioteca lato e insere no objeto do FastAPI
set_lato_app(api)

@api.get("/", status_code=HTTPStatus.OK)
def root(app: Annotated[Application, Depends(get_lato_app)]):
    return {"message": "Hello World!"}


if __name__ == "__main__":
    uvicorn.run("main:api", host="0.0.0.0", port=8000, reload=True)
