from fazaconta_backend.modules.group.domain.Transaction import Transaction
from fazaconta_backend.modules.group.infra.models.TransactionDocument import (
    TransactionDocument,
)
from fazaconta_backend.modules.group.repos.ITransactionRepo import (
    ITransactionRepo,
)
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.infra.database.mongodb.AbstractMongoGenericRepository import (
    AbstractMongoGenericRepository,
)


class MongoTransactionRepo(
    AbstractMongoGenericRepository[Transaction, TransactionDocument], ITransactionRepo
):
    async def get_by_group_id(
        self, group_id: UniqueEntityId, limit: int, skip: int
    ) -> list[Transaction] | None:

        transactions = (
            await self._model_cls.find(
                self._model_cls.group.id == group_id.value,
                fetch_links=True,
                session=self._session,
            )
            .limit(limit)
            .skip(skip)
            .to_list()
        )

        return [await self._mapper.to_domain(t) for t in transactions]
