from collections.abc import Callable
from typing import Any

from fastapi import FastAPI, Request
from lato import Application, TransactionContext


def set_lato_app(app: FastAPI):
    app.lato_app = create_lato_app()


def get_lato_app(request: Request) -> Application:

    app = request.app.lato_app
    return app


def create_lato_app() -> Application:
    app = Application("FazAConta")

    # Exemplo para incluir modulos
    # app.include_submodule(<nome_modulo>)

    @app.on_enter_transaction_context
    def on_enter_transaction_context(ctx: TransactionContext):
        # Exemplo de pegar dependência pelo context
        # logger = ctx["logger"]

        print("Begin transaction")

        # Exemplo de setar uma nova depedência
        # ctx.set_dependencies(
        #     now=datetime.now(),
        # )

    @app.on_exit_transaction_context
    def on_exit_transaction_context(ctx: TransactionContext, exception=None):
        print("End transaction")

    @app.transaction_middleware
    def logging_middleware(ctx: TransactionContext, call_next: Callable) -> Any:
        print(ctx.resolved_kwargs)
        handler = ctx.current_handler
        message_name = ctx.get_dependency("message").__class__.__name__
        handler_name = f"{handler.source}.{handler.fn.__name__}"

        print(f"Executing {handler_name}({message_name})")
        result = call_next()
        print(f"Result from {handler_name}: {result}")
        return result

    return app
