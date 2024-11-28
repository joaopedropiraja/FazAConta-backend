from uuid import UUID, uuid4
from Identifier import Identifier


class UniqueEntityId(Identifier[UUID | int]):
    def __init__(self, id: UUID | int | None = None):
        super().__init__(uuid4() if id is None else id)
