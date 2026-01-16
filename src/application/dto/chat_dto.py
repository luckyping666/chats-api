from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ChatCreateDTO(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Chat title",
    )

    @field_validator("title")
    @classmethod
    def strip_title(cls, value: str) -> str:
        return value.strip()


class ChatDTO(BaseModel):
    id: int
    title: str
    created_at: datetime
