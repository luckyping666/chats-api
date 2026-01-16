from datetime import datetime
from typing import Optional

from src.domain.exceptions import ValidationError


class Chat:
    def __init__(
        self,
        title: str,
        id: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ) -> None:
        title = title.strip()

        if not title:
            raise ValidationError("Chat title must not be empty")

        if not (1 <= len(title) <= 200):
            raise ValidationError("Chat title length must be between 1 and 200")

        self.id = id
        self.title = title
        self.created_at = created_at
