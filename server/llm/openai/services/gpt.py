import asyncio
from typing import Any, Dict, List

import openai
from openai import OpenAI

from server.llm.openai.config import OpenAISettings
from server.llm.openai.schemas.gpt_answer import StructuredOutput
from server.llm.openai.utils.gpt_answer import format_response
from server.core.logging.config import setup_logging

logger = setup_logging(__name__)

class OpenAILLM:
    def __init__(
        self,
        api_key: str,
        settings: OpenAISettings,
    ):
        self.client = OpenAI(api_key=api_key)
        self.settings = settings

    def set_api_key(self, api_key: str) -> bool:
        """NOTE : 올바른 api key 인지 확인하고, api key 세팅하기"""
        # 1) api 세팅
        self.api_key = api_key

        # 2) api key 맞는지 확인
        try:
            # TODO: The resource 'Engine' has been deprecated
            # openai.Engine.list()
            logger.info(f"Success to set an api key for OpenAI.")
            return True
        except openai.AuthenticationError:
            logger.error(f"Failed to set an api key for OpenAI.")
            return False

    def generate(self, messages: List[Dict[str, Any]]) -> str:
        """NOTE : llm 답변 받기"""
        response = self.client.chat.completions.create(
            model=self.settings.OPENAI_LLM_MODEL, messages=messages
        )
        logger.info(f"Success to get a response from openai.\n{response}")
        return response.choices[0].message.content

    async def generate_streaming(self, messages: List[Dict[str, Any]]) -> str:
        """NOTE : llm 답변 받기"""
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
        response = self.client.beta.chat.completions.parse(
            model=self.settings.OPENAI_LLM_MODEL,
            messages=messages,
            response_format=StructuredOutput,
        )
        logger.info(f"Success to get a response from openai.\n{response}")
        
        response = format_response(response.choices[0].message.parsed)

        for chunk in response:
            yield chunk
            await asyncio.sleep(0.1)
