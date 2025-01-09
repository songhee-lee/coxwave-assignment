from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from server.modules.chat.schemas.request import ChatRequest
from server.modules.chat.schemas.response import ChatResponse
from server.modules.chat.services.rag import get_chat_response

router = APIRouter()

@router.post("/chat")
async def chat(request: ChatRequest) -> ChatResponse :
    try:
        generated_text = get_chat_response(
            collection_name=request.service, 
            messages=request.messages,
            stream=False
        )
        return {
            "taskId" : request.taskId,
            "generated_text": generated_text
        }
    except Exception as e:
        return {
            "taskId" : request.taskId,
            "error" : str(e)
        }

@router.post("/chat_stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse :
    try:
        response_stream = get_chat_response(
            collection_name=request.service, 
            messages=request.messages,
            stream=True
        )

        return StreamingResponse(
            response_stream, media_type="text/plain"
        )

    except Exception as e:
        return {
            "taskId" : request.taskId,
            "error" : str(e)
        }