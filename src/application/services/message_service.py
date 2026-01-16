from src.application.dto import MessageCreateDTO, MessageDTO
from src.domain.exceptions import ChatNotFound
from src.domain.entities import Message
from src.domain.repositories import ChatRepository, MessageRepository


class MessageService:
    def __init__(
        self,
        chat_repository: ChatRepository,
        message_repository: MessageRepository,
    ) -> None:
        self._chat_repository = chat_repository
        self._message_repository = message_repository

    async def send_message(
        self,
        chat_id: int,
        dto: MessageCreateDTO,
    ) -> MessageDTO:
        chat = await self._chat_repository.get_by_id(chat_id)
        if chat is None:
            raise ChatNotFound(f"Chat with id={chat_id} not found")

        message = Message(
            id=0,  # временный
            chat_id=chat_id,
            text=dto.text,
            created_at=None,  # заполнит БД
        )

        created_message = await self._message_repository.create(message)

        return MessageDTO(
            id=created_message.id,
            chat_id=created_message.chat_id,
            text=created_message.text,
            created_at=created_message.created_at,
        )
