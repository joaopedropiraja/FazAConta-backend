from fastapi import Request


class UnitOfWork:
    def __call__(self, request: Request):
        return request.state.uow
