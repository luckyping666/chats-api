from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.chat import Chat


class ChatRepository(ABC):
    @abstractmethod
    async def create(self, chat: Chat) -> Chat:
        """Create a new chat."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, chat_id: int) -> Optional[Chat]:
        """Return chat by id or None if not found."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, chat_id: int) -> None:
        """Delete chat by id."""
        raise NotImplementedError
