from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import Chat
from src.domain.repositories import ChatRepository
from src.infrastructure.db.models import ChatModel


class SqlAlchemyChatRepository(ChatRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, chat: Chat) -> Chat:
        model = ChatModel(
            title=chat.title,
        )

        self._session.add(model)
        await self._session.flush()

        return Chat(
            id=model.id,
            title=model.title,
            created_at=model.created_at,
        )

    async def get_by_id(self, chat_id: int) -> Chat | None:
        stmt = select(ChatModel).where(ChatModel.id == chat_id)
        result = await self._session.execute(stmt)

        model: ChatModel | None = result.scalar_one_or_none()
        if model is None:
            return None

        return Chat(
            id=model.id,
            title=model.title,
            created_at=model.created_at,
        )

    async def delete(self, chat_id: int) -> None:
        stmt = delete(ChatModel).where(ChatModel.id == chat_id)
        await self._session.execute(stmt)
