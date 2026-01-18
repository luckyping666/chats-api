from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.api.dependencies import get_chat_service, get_message_service
from src.application.dto.chat_dto import ChatCreateDTO, ChatDTO
from src.application.dto.message_dto import MessageDTO, MessageCreateDTO
from src.application.services.chat_service import ChatService
from src.application.services.message_service import MessageService
from src.domain.exceptions import ChatNotFound, ValidationError

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", response_model=ChatDTO, status_code=status.HTTP_201_CREATED)
async def create_chat(dto: ChatCreateDTO, service: ChatService = Depends(get_chat_service)) -> ChatDTO:
    try:
        return await service.create_chat(dto)
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.post("/{chat_id}/messages/", response_model=MessageDTO, status_code=status.HTTP_201_CREATED)
async def send_message(chat_id: int, dto: MessageCreateDTO, service: MessageService = Depends(get_message_service)) -> MessageDTO:
    try:
        return await service.send_message(chat_id, dto)
    except ChatNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    except ValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get("/{chat_id}", status_code=status.HTTP_200_OK)
async def get_chat(chat_id: int, limit: int = Query(20, ge=1, le=100), service: ChatService = Depends(get_chat_service)):
    try:
        chat, messages = await service.get_chat(chat_id, limit)
        return {
            "chat": chat,
            "messages": messages,
        }
    except ChatNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(chat_id: int, service: ChatService = Depends(get_chat_service)) -> None:
    try:
        await service.delete_chat(chat_id)
    except ChatNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
