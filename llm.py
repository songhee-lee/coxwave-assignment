import openai
from typing import List, Dict, Any

from config import settings
from db import db

class LLM:
    def set_api_key(self, api_key: str) -> None:
        """NOTE : 올바른 api key 인지 확인하고, api key 세팅하기 """
        # 1) api 세팅
        self.api_key = api_key
        openai.api_key = api_key

        # 2) api key 맞는지 확인
        try :
            openai.Engine.list()
            return True
        except openai.error.AuthenticationError :
            return False

    def generate(self, messages: List[Dict[str, Any]]) -> str:
        """NOTE : llm 답변 받기 """
        # 1) RAG - context 찾기
        query = messages[-1]['content']
        context = "\n".join(db.get_relevant_context(query)[0])
        messages[-1]["content"] = f"{settings.prompt.RAG_PROMPT}\nContext: {context}\nQuery: {messages[-1]['content']}"

        # 2) LLM 응답
        response = openai.ChatCompletion.create(
            model=settings.llm.GPT_MODEL,
            messages=messages
        )

        # 3) 기존 메세지 복구 (RAG context 추가 전)
        messages[-1]["content"] = query
        
        # 4) response
        return response.choices[0].message["content"]

llm = LLM()