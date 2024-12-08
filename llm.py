import openai
from typing import List, Dict, Any

from config import settings

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
        response = openai.ChatCompletion.create(
            model=settings.llm.GPT_MODEL,
            messages=messages
        )
        return response.choices[0].message["content"]

llm = LLM()
