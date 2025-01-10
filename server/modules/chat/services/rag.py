from typing import Any, Dict, List

from server.db.chromadb.services.database import ChromaDB
from server.llm.openai.services.gpt import OpenAILLM
from server.modules.chat.config import ChatSettings


def organize_messages(
    collection_name: str,
    messages: List[Dict[str, Any]],
    db: ChromaDB,
    settings: ChatSettings,
) -> List[Dict[str, Any]]:
    """NOTE : 사용자 메세지에 시스템 메세지와 RAG 후 context 추가하기"""

    # 1) 시스템 프롬프트 추가하기
    messages[0]["content"] = settings.SYSTEM_PROMPT

    # 2) RAG - context 찾아서 마지막 메세지에 추가하기
    query = messages[-1]["content"]
    contexts = db.get_relevant_context(collection_name, query)
    context = "\n".join(contexts)

    messages[-1]["content"] = (
        f"{settings.RAG_PROMPT}\nContext: {context}\nQuery: {messages[-1]['content']}"
    )
    return messages


def get_chat_response(
    collection_name: str,
    messages: List[Dict[str, Any]],
    db: ChromaDB,
    llm: OpenAILLM,
    settings: ChatSettings,
    stream=True,
) -> str:
    # 1) 메세지 확인
    messages = organize_messages(
        collection_name=collection_name, messages=messages, db=db, settings=settings
    )

    # 2) LLM 답변
    if stream:
        return llm.generate_streaming(messages)
