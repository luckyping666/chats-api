from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services import ChatService, MessageService
from src.core.database import get_session
from src.infrastructure.db.repositories import (
    SqlAlchemyChatRepository,
    SqlAlchemyMessageRepository,
)


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
