from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.chat_service import ChatService
from src.application.services.message_service import MessageService
from src.core.database import get_session

from src.infrastructure.db.repositories.chat_repo import SqlAlchemyChatRepository
from src.infrastructure.db.repositories.message_repo import SqlAlchemyMessageRepository

def get_chat_service(
    session: AsyncSession = Depends(get_session),
) -> ChatService:
    chat_repo = SqlAlchemyChatRepository(session)
    message_repo = SqlAlchemyMessageRepository(session)
    return ChatService(chat_repo, message_repo)


def get_message_service(
    session: AsyncSession = Depends(get_session),
) -> MessageService:
    chat_repo = SqlAlchemyChatRepository(session)
    message_repo = SqlAlchemyMessageRepository(session)
    return MessageService(chat_repo, message_repo)
