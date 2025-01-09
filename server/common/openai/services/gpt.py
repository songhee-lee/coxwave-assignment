import openai
from openai import OpenAI
import json
from typing import List, Dict, Any
import asyncio

from server.common.openai.config import openai_settings
from server.common.openai.schemas.gpt_answer import StructuredOutput
from server.common.openai.utils.gpt_answer import format_response


client = OpenAI(api_key=openai_settings.OPENAI_API_KEY)
class LLM:
    def set_api_key(self, api_key: str) -> bool:
        """NOTE : 올바른 api key 인지 확인하고, api key 세팅하기 """
        # 1) api 세팅
        self.api_key = api_key

        # 2) api key 맞는지 확인
        try :
            # TODO: The resource 'Engine' has been deprecated
            # openai.Engine.list()
            return True
        except openai.AuthenticationError :
            return False

    def generate(self, messages: List[Dict[str, Any]]) -> str:
        """NOTE : llm 답변 받기 """
        response = client.chat.completions.create(model=openai_settings.OPENAI_LLM_MODEL,
        messages=messages)

        return response.choices[0].message.content

    async def generate_streaming(self, messages: List[Dict[str, Any]]) -> str:
        """NOTE : llm 답변 받기 """
        # with client.beta.chat.completions.stream(
        #     model=openai_settings.OPENAI_LLM_MODEL,
        #     messages=messages,
        #     response_format=StructuredOutput,
        #     stream_options={"include_usage" : True}
        # ) as stream :
        #     for idx, chunk in enumerate(stream) :
        #         if chunk.type == "content.delta" and idx >= 11:
        #             formatted_response = await format_response(chunk.delta)
        #             yield formatted_response
        #             #yield make_answer(chunk.content)
        #         await asyncio.sleep(0.1)
        response = client.beta.chat.completions.parse(
            model=openai_settings.OPENAI_LLM_MODEL,
            messages=messages,
            response_format=StructuredOutput,
        )
        print(response.choices[0].message.parsed)
        response = format_response(response.choices[0].message.parsed)
        
        for chunk in response :
            yield chunk
            await asyncio.sleep(0.1)

openai_llm = LLM()