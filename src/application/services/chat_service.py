from src.application.dto.chat_dto import ChatCreateDTO, ChatDTO
from src.application.dto.message_dto import MessageDTO
from src.domain.exceptions import ChatNotFound
from src.domain.entities.chat import Chat
from src.domain.repositories.chat_repo import ChatRepository
from src.domain.repositories.message_repo import MessageRepository

class ChatService:
    def __init__(
        self,
        chat_repository: ChatRepository,
        message_repository: MessageRepository,
    ) -> None:
        self._chat_repository = chat_repository
        self._message_repository = message_repository

    async def create_chat(self, dto: ChatCreateDTO) -> ChatDTO:
        chat = Chat(title=dto.title)

        created_chat = await self._chat_repository.create(chat)

        return ChatDTO(
            id=created_chat.id,
            title=created_chat.title,
            created_at=created_chat.created_at,
        )

    async def get_chat(
        self,
        chat_id: int,
        limit: int = 20,
    ) -> tuple[ChatDTO, list[MessageDTO]]:
        limit = min(limit, 100)

        chat = await self._chat_repository.get_by_id(chat_id)
        if chat is None:
            raise ChatNotFound(f"Chat with id={chat_id} not found")

        messages = await self._message_repository.get_last_by_chat(
            chat_id=chat_id,
            limit=limit,
        )

        return (
            ChatDTO(
                id=chat.id,
                title=chat.title,
                created_at=chat.created_at,
            ),
            [
                MessageDTO(
                    id=m.id,
                    chat_id=m.chat_id,
                    text=m.text,
                    created_at=m.created_at,
                )
                for m in messages
            ],
        )

    async def delete_chat(self, chat_id: int) -> None:
        chat = await self._chat_repository.get_by_id(chat_id)
        if chat is None:
            raise ChatNotFound(f"Chat with id={chat_id} not found")

        await self._chat_repository.delete(chat_id)
