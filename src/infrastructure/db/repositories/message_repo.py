from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.message import Message
from src.domain.repositories.message_repo import MessageRepository
from src.infrastructure.db.models.message_model import MessageModel


class SqlAlchemyMessageRepository(MessageRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, message: Message) -> Message:
        model = MessageModel(
            chat_id=message.chat_id,
            text=message.text,
        )

        self._session.add(model)
        await self._session.flush()

        return Message(
            id=model.id,
            chat_id=model.chat_id,
            text=model.text,
            created_at=model.created_at,
        )

    async def get_last_by_chat(
        self,
        chat_id: int,
        limit: int,
    ) -> list[Message]:
        stmt = (
            select(MessageModel)
            .where(MessageModel.chat_id == chat_id)
            .order_by(MessageModel.created_at.desc())
            .limit(limit)
        )

        result = await self._session.execute(stmt)
        models = result.scalars().all()

        return [
            Message(
                id=m.id,
                chat_id=m.chat_id,
                text=m.text,
                created_at=m.created_at,
            )
            for m in reversed(models)  # ASC по created_at
        ]

    async def delete_by_chat(self, chat_id: int) -> None:
        stmt = delete(MessageModel).where(MessageModel.chat_id == chat_id)
        await self._session.execute(stmt)
