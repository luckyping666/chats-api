from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class MessageCreateDTO(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Message text",
    )

    @field_validator("text")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class MessageDTO(BaseModel):
    id: int
    chat_id: int
    text: str
    created_at: datetime
