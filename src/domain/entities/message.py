from datetime import datetime
from typing import Optional

from src.domain.exceptions import ValidationError


class Message:
    def __init__(
        self,
        chat_id: int,
        text: str,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        text = text.strip()

        if not text:
            raise ValidationError("Message text must not be empty")

        if not (1 <= len(text) <= 5000):
            raise ValidationError("Message text length must be between 1 and 5000")

        self.id = id
        self.chat_id = chat_id
        self.text = text
        self.created_at = created_at
