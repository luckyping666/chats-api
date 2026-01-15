from datetime import datetime

from domain.exceptions import ValidationError


class Message:
    def __init__(
        self,
        id: int,
        chat_id: int,
        text: str,
        created_at: datetime,
    ) -> None:
        text = text.strip()

        if not text:
            raise ValidationError("Message text must not be empty")

        if not (1 <= len(text) <= 5000):
            raise ValidationError("Message text length must be between 1 and 5000")

        self.id: int = id
        self.chat_id: int = chat_id
        self.text: str = text
        self.created_at: datetime = created_at
