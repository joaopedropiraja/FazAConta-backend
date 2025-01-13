from typing import Annotated
from uuid import UUID
from click import group
from fastapi import APIRouter, Body, Depends, Query, status
from fastapi.responses import JSONResponse

from fazaconta_backend.modules.group.dtos.TransactionDTO import TransactionDTO

from fazaconta_backend.modules.group.useCases.transaction.createTransaction.CreateTransactionDTO import (
    CreateTransactionDTO,
    CreateTransactionRequest,
)
from fazaconta_backend.modules.group.useCases.transaction.createTransaction.CreateTransactionExceptions import (
    GroupNotFoundException,
)

from fazaconta_backend.modules.group.useCases.transaction.createTransaction.CreateTransactionUseCase import (
    CreateTransactionUseCase,
)
from fazaconta_backend.modules.group.useCases.transaction.getTransactionsByGroupId.GetTransactionsByGroupIdDTO import (
    GetTransactionsByGroupIdDTO,
)
from fazaconta_backend.modules.group.useCases.transaction.getTransactionsByGroupId.GetTransactionsByGroupIdUseCase import (
    GetTransactionsByGroupIdUseCase,
)
from fazaconta_backend.modules.user.domain.jwt import JWTData
from fazaconta_backend.shared.infra.database.IUnitOfWork import (
    IUnitOfWork,
)
from fazaconta_backend.shared.infra.http.dependencies import JWTBearer, UnitOfWork


transactions_router = APIRouter()
route = "/transactions"


@transactions_router.post(
    route,
    status_code=status.HTTP_201_CREATED,
    response_model=TransactionDTO,
    tags=["transactions"],
)
async def create_transaction(
    uow: Annotated[IUnitOfWork, Depends(UnitOfWork())],
    jwt_data: Annotated[JWTData, Depends(JWTBearer())],
    body: Annotated[CreateTransactionRequest, Body()],
) -> TransactionDTO | JSONResponse:
    try:
        use_case = CreateTransactionUseCase(uow)
        dto = CreateTransactionDTO(
            **body.model_dump(), paid_by_user_id=jwt_data.user.id
        )

        return await use_case.execute(dto)
    except GroupNotFoundException as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": "Not found",
                "errors": str(exc),
            },
        )


@transactions_router.get(
    f"{route}/{{group_id}}/groups",
    status_code=status.HTTP_200_OK,
    response_model=list[TransactionDTO],
    tags=["transaction"],
)
async def get_transactions_by_group_id(
    uow: Annotated[IUnitOfWork, Depends(UnitOfWork())],
    jwt_data: Annotated[JWTData, Depends(JWTBearer())],
    group_id: UUID,
    limit: Annotated[int, Query()] = 0,
    skip: Annotated[int, Query()] = 0,
) -> list[TransactionDTO] | JSONResponse:

    try:
        use_case = GetTransactionsByGroupIdUseCase(uow)
        dto = GetTransactionsByGroupIdDTO(
            group_id=group_id, logged_user_id=jwt_data.user.id, limit=limit, skip=skip
        )
        return await use_case.execute(dto)
    except GroupNotFoundException as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": "Not found",
                "errors": str(exc),
            },
        )
