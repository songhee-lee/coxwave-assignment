import openai
from typing import List, Dict, Any
import asyncio

from server.common.openai.config import openai_settings

class LLM:
    def set_api_key(self, api_key: str) -> bool:
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
        response = openai.ChatCompletion.create(
            model=openai_settings.OPENAI_LLM_MODEL,
            messages=messages
        )

        return response.choices[0].message["content"]

    async def generate_streaming(self, messages: List[Dict[str, Any]]) -> str:
        """NOTE : llm 답변 받기 """
        response = openai.ChatCompletion.create(
            model=openai_settings.OPENAI_LLM_MODEL,
            messages=messages,
            stream=True
        )

        for chunk in response :
            content = chunk["choices"][0].delta.get("content","")
            if content :
                yield content
                await asyncio.sleep(0.1)

openai_llm = LLM()