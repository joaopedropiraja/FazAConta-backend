from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi.responses import JSONResponse

from fazaconta_backend.modules.group.domain.Group import Group
from fazaconta_backend.modules.group.infra.models.GroupDocument import GroupDocument
from fazaconta_backend.modules.group.infra.models.MemberDocument import MemberDocument
from fazaconta_backend.modules.user.domain.UserDetail import UserDetail
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.AbstractUnitOfWork import (
    AbstractUnitOfWork,
)
from fazaconta_backend.shared.infra.http.dependencies import UnitOfWork


groups_router = APIRouter()
route = "/group"


@groups_router.post(
    route,
    status_code=status.HTTP_201_CREATED,
    # response_model=TransferenceDTO,
    tags=["group"],
)
async def create_group(
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork())],
    title: Annotated[str, Form()],
    image: Annotated[UploadFile | None, File()] = None,
    # dto: Annotated[CreateTransferenceDTO, Body()],
):  # -> TransferenceDTO | JSONResponse:

    async with uow as uow_conn:
        doc = await GroupDocument.get(
            "a03bf5ed-6a48-4066-849c-43fe816504cd", fetch_links=True
        )
        print(doc)
        # logged_user = await uow_conn.users.get_by_id(
        #     UniqueEntityId(UUID("151de6be-f7ac-4515-a4d2-b8e1c4ec5015"))
        # )
        # created_by = UserDetail(
        #     user_id=logged_user.id.value,
        #     email=logged_user.email.value,
        #     nickname=logged_user.nickname,
        # )
        # group = Group(title=title, created_by=created_by)
        # group_doc = GroupDocument(
        #     title=title,
        #     created_by=logged_user.id.value,
        #     created_at=group.created_at,
        #     total_expense=group.total_expense,
        # )
        # await group_doc.save()

        # member_doc = MemberDocument(
        #     user=logged_user.id.value, group=group_doc.id, balance=0.0
        # )
        # await member_doc.save()

        # # await group_doc.fetch_all_links()

        # print(group_doc)

    return JSONResponse(doc)

    # try:
    #     use_case = CreateTransferenceUseCase(uow)

    #     return await use_case.execute(dto)
    # except GroupNotFoundException as exc:
    #     return JSONResponse(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         content={
    #             "message": "Not found",
    #             "errors": str(exc),
    #         },
    #     )
    # except ParticipantsTotalAmountNotEqualToTransferenceAmountException as exc:
    #     return JSONResponse(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         content={
    #             "message": "Bad request",
    #             "errors": str(exc),
    #         },
    #     )


@groups_router.get(
    "/groups",
    status_code=status.HTTP_200_OK,
    # response_model=TransferenceDTO,
    tags=["groups"],
)
async def get_groups(
    uow: Annotated[AbstractUnitOfWork, Depends(UnitOfWork())],
    # dto: Annotated[CreateTransferenceDTO, Body()],
):  # -> TransferenceDTO | JSONResponse:
    return []
