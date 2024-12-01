from uuid import UUID, uuid4
from fazaconta_backend.shared.domain.Identifier import Identifier


class UniqueEntityId(Identifier[UUID]):
    def __init__(self, id: UUID | None = None):
        super().__init__(uuid4() if id is None else id)
