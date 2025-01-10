from typing import Annotated
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from fazaconta_backend.modules.transference.domain.exceptions import (
    ParticipantsTotalAmountNotEqualToTransferenceAmountException,
)
from fazaconta_backend.modules.transference.dtos.TransferenceDTO import TransferenceDTO
from fazaconta_backend.modules.transference.useCases.createTransference.CreateTransferenceDTO import (
    CreateTransferenceDTO,
)
from fazaconta_backend.modules.transference.useCases.createTransference.CreateTransferenceExceptions import (
    GroupNotFoundException,
)
from fazaconta_backend.modules.transference.useCases.createTransference.CreateTransferenceUseCase import (
    CreateTransferenceUseCase,
)
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)
from fazaconta_backend.shared.infra.http.dependencies import UnitOfWork


transferences_router = APIRouter()


@transferences_router.post(
    "/transferences",
    status_code=status.HTTP_201_CREATED,
    response_model=TransferenceDTO,
    tags=["transferences"],
)
async def create_transference(
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork())],
    dto: Annotated[CreateTransferenceDTO, Body()],
) -> TransferenceDTO | JSONResponse:

    try:
        use_case = CreateTransferenceUseCase(uow)

        return await use_case.execute(dto)
    except GroupNotFoundException as exc:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "message": "Not found",
                "errors": str(exc),
            },
        )
    except ParticipantsTotalAmountNotEqualToTransferenceAmountException as exc:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "Bad request",
                "errors": str(exc),
            },
        )
