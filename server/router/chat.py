from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from server.db.chromadb.services import ChromaDB
from server.dependencies import get_chat_settings, get_chromadb_service, get_llm_service
from server.llm.openai.services import OpenAILLM
from server.modules.chat import ChatSettings
from server.modules.chat.schemas import ChatRequest, ChatResponse
from server.modules.chat.services import get_chat_response
from server.core.logging.config import setup_logging

logger = setup_logging(__name__)

router = APIRouter()


@router.post("/chat")
async def chat(
    request: ChatRequest,
    db: ChromaDB = Depends(get_chromadb_service),
    llm: OpenAILLM = Depends(get_llm_service),
    settings: ChatSettings = Depends(get_chat_settings),
) -> ChatResponse:
    try:
        generated_text = get_chat_response(
            collection_name=request.service,
            messages=request.messages,
            db=db,
            llm=llm,
            settings=settings,
            stream=False,
        )
        return {"taskId": request.task_id, "generated_text": generated_text}
    except Exception as e:
        logger.error(f"Failed get_chat_resonse : {str(e)}")
        return {"taskId": request.task_id, "error": str(e)}


@router.post("/chat_stream")
async def chat_stream(
    request: ChatRequest,
    db: ChromaDB = Depends(get_chromadb_service),
    llm: OpenAILLM = Depends(get_llm_service),
    settings: ChatSettings = Depends(get_chat_settings),
) -> StreamingResponse:
    try:
        response_stream = get_chat_response(
            collection_name=request.service,
            messages=request.messages,
            db=db,
            llm=llm,
            settings=settings,
            stream=True,
        )

        return StreamingResponse(response_stream, media_type="text/plain")

    except Exception as e:
        logger.error(f"Failed get_chat_resonse : {str(e)}")
        return {"taskId": request.task_id, "error": str(e)}
