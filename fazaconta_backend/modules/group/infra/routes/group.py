from typing import Annotated
from uuid import UUID
from click import group
from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from fastapi.responses import JSONResponse

from fazaconta_backend.modules.group.dtos.GroupDTO import GroupDTO
from fazaconta_backend.modules.group.useCases.group.addMember.AddMemberDTO import (
    AddMemberDTO,
)
from fazaconta_backend.modules.group.useCases.group.addMember.AddMemberUseCase import (
    AddMemberUseCase,
)
from fazaconta_backend.modules.group.useCases.group.createGroup.CreateGroupUseCase import (
    CreateGroupUseCase,
)
from fazaconta_backend.modules.group.useCases.group.createGroup.CreateGroupUseCaseDTO import (
    CreateGroupUseCaseDTO,
)
from fazaconta_backend.modules.group.useCases.group.getGroupById.GetGroupByIdDTO import (
    GetGroupByIdDTO,
    GetGroupByIdFullResponse,
    GetGroupByIdLimitedResponse,
)
from fazaconta_backend.modules.group.useCases.group.getGroupById.GetGroupByIdUseCase import (
    GetGroupByIdUseCase,
)
from fazaconta_backend.modules.group.useCases.group.getGroupsByUserId.GetGroupsByUserIdDTO import (
    GetGroupByUserIdResponse,
    GetGroupsByUserIdDTO,
)
from fazaconta_backend.modules.group.useCases.group.getGroupsByUserId.GetGroupsByUserIdUseCase import (
    GetGroupsByUserIdUseCase,
)
from fazaconta_backend.modules.user.domain.jwt import JWTData
from fazaconta_backend.shared.domain.files.IFileHandler import (
    IFileHandler,
)
from fazaconta_backend.shared.infra.database.IUnitOfWork import (
    IUnitOfWork,
)
from fazaconta_backend.shared.infra.http.dependencies import (
    FileHandler,
    JWTBearer,
    UnitOfWork,
)


groups_router = APIRouter()
route = "/groups"


@groups_router.post(
    route,
    status_code=status.HTTP_201_CREATED,
    response_model=GroupDTO,
    tags=["groups"],
)
async def create_group(
    uow: Annotated[IUnitOfWork, Depends(UnitOfWork())],
    file_handler: Annotated[IFileHandler, Depends(FileHandler())],
    jwt_data: Annotated[JWTData, Depends(JWTBearer())],
    title: Annotated[str, Form()],
    image: Annotated[UploadFile | None, File()] = None,
) -> GroupDTO:
    dto = CreateGroupUseCaseDTO(
        created_by_user_id=jwt_data.user.id,
        title=title,
        image=image,
    )
    use_case = CreateGroupUseCase(uow=uow, file_handler=file_handler)

    return await use_case.execute(dto)


@groups_router.get(
    f"{route}/users",
    status_code=status.HTTP_200_OK,
    response_model=list[GetGroupByUserIdResponse],
    tags=["groups"],
)
async def get_groups_by_user_id(
    uow: Annotated[IUnitOfWork, Depends(UnitOfWork())],
    jwt_data: Annotated[JWTData, Depends(JWTBearer())],
    limit: Annotated[int, Query()] = 0,
    skip: Annotated[int, Query()] = 0,
) -> list[GetGroupByUserIdResponse] | JSONResponse:
    use_case = GetGroupsByUserIdUseCase(uow=uow)
    dto = GetGroupsByUserIdDTO(user_id=jwt_data.user.id, limit=limit, skip=skip)

    return await use_case.execute(dto)


@groups_router.get(
    f"{route}/{{group_id}}/users",
    status_code=status.HTTP_200_OK,
    response_model=GroupDTO,
    tags=["groups"],
)
async def add_member(
    uow: Annotated[IUnitOfWork, Depends(UnitOfWork())],
    jwt_data: Annotated[JWTData, Depends(JWTBearer())],
    group_id: UUID,
) -> GroupDTO:
    use_case = AddMemberUseCase(uow=uow)
    dto = AddMemberDTO(user_id=jwt_data.user.id, group_id=group_id)
    return await use_case.execute(dto)


@groups_router.get(
    f"{route}/{{group_id}}",
    status_code=status.HTTP_200_OK,
    response_model=GetGroupByIdLimitedResponse | GetGroupByIdFullResponse,
    tags=["groups"],
)
async def get_group_by_id(
    uow: Annotated[IUnitOfWork, Depends(UnitOfWork())],
    jwt_data: Annotated[JWTData, Depends(JWTBearer())],
    group_id: UUID,
) -> GetGroupByIdLimitedResponse | GetGroupByIdFullResponse:
    use_case = GetGroupByIdUseCase(uow=uow)
    dto = GetGroupByIdDTO(user_id=jwt_data.user.id, group_id=group_id)
    return await use_case.execute(dto)
