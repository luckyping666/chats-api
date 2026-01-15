from datetime import datetime

from domain.exceptions import ValidationError


class Chat:
    def __init__(self, id: int, title: str, created_at: datetime) -> None:
        title = title.strip()

        if not title:
            raise ValidationError("Chat title must not be empty")

        if not (1 <= len(title) <= 200):
            raise ValidationError("Chat title length must be between 1 and 200")

        self.id: int = id
        self.title: str = title
        self.created_at: datetime = created_at
