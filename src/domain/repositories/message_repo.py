from abc import ABC, abstractmethod
from typing import List

from src.domain.entities import Message


class MessageRepository(ABC):
    @abstractmethod
    async def create(self, message: Message) -> Message:
        """Create a new message."""
        raise NotImplementedError

    @abstractmethod
    async def get_last_by_chat(
        self,
        chat_id: int,
        limit: int,
    ) -> List[Message]:
        """Return last messages for a chat ordered by created_at."""
        raise NotImplementedError

    @abstractmethod
    async def delete_by_chat(self, chat_id: int) -> None:
        """Delete all messages for a chat."""
        raise NotImplementedError
