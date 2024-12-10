from typing import List, Dict, Any

from server.modules.chat.config import chat_settings
from server.common.chromadb.services.database import chroma_db
from server.common.openai.services.gpt import openai_llm

def organize_messages(collection_name, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """NOTE : 사용자 메세지에 시스템 메세지와 RAG 후 context 추가하기 """

    # 1) 시스템 프롬프트 추가하기
    messages[0]["content"] = chat_settings.SYSTEM_PROMPT

    # 2) RAG - context 찾아서 마지막 메세지에 추가하기
    query = messages[-1]['content']
    contexts = chroma_db.get_relevant_context(collection_name, query)
    context = "\n".join(contexts)

    messages[-1]["content"] = f"{chat_settings.RAG_PROMPT}\nContext: {context}\nQuery: {messages[-1]["content"]}"
    return messages
    

def get_chat_response(collection_name, messages: List[Dict[str, Any]]) -> str:
        
        # 1) 메세지 확인
        messages = organize_messages(collection_name, messages)

        # 2) LLM 답변
        return openai_llm.generate(messages)