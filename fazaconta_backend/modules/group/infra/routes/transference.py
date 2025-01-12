from typing import Annotated
from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from fazaconta_backend.modules.group.dtos.TransferenceDTO import TransferenceDTO

from fazaconta_backend.modules.group.useCases.transference.createTransference.CreateTransferenceDTO import (
    CreateTransferenceDTO,
    CreateTransferenceRequest,
)
from fazaconta_backend.modules.group.useCases.transference.createTransference.CreateTransferenceExceptions import (
    GroupNotFoundException,
)

from fazaconta_backend.modules.group.useCases.transference.createTransference.CreateTransferenceUseCase import (
    CreateTransferenceUseCase,
)
from fazaconta_backend.modules.user.domain.jwt import JWTData
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)
from fazaconta_backend.shared.infra.http.dependencies import JWTBearer, UnitOfWork


transferences_router = APIRouter()
route = "/transferences"


@transferences_router.post(
    route,
    status_code=status.HTTP_201_CREATED,
    response_model=TransferenceDTO,
    tags=["transferences"],
)
async def create_transference(
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork())],
    jwt_data: Annotated[JWTData, Depends(JWTBearer())],
    body: Annotated[CreateTransferenceRequest, Body()],
) -> TransferenceDTO | JSONResponse:
    try:
        use_case = CreateTransferenceUseCase(uow)
        dto = CreateTransferenceDTO(
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


# @transferences_router.get(
#     f"{route}/{{group_id}}/groups",
#     status_code=status.HTTP_200_OK,
#     response_model=list[TransferenceDTO],
#     tags=["transference"],
# )
# async def get_transferences_by_group_id(
#     uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork())],
#     group_id: UUID
# ) -> list[TransferenceDTO] | JSONResponse:

#     try:
#         use_case = GetTransferencesByGroupId(uow)
#   dto = GetTrans
#         return await use_case.execute(group_id)
#     except GroupNotFoundException as exc:
#         return JSONResponse(
#             status_code=status.HTTP_404_NOT_FOUND,
#             content={
#                 "message": "Not found",
#                 "errors": str(exc),
#             },
#         )
