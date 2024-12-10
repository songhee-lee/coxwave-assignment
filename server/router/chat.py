from fastapi import APIRouter

from server.modules.chat.dtos.request import ChatRequest
from server.modules.chat.dtos.response import ChatResponse
from server.modules.chat.services.rag import get_chat_response

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse :
    try:
        generated_text = get_chat_response(request.service, request.messages)
        return {
            "taskId" : request.taskId,
            "generated_text": generated_text
        }
    except Exception as e:
        return {
            "taskId" : request.taskId,
            "error" : str(e)
        }