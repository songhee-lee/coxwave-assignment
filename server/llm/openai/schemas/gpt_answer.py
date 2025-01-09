from pydantic import BaseModel, Field
from typing import List

class StructuredOutput(BaseModel):
    answer: str = Field(description="사용자 질문에 대한 답변")
    additional_questions: List[str] = Field(description="질의응답 맥락에서 사용자가 궁금해 할만한 다른 질문, 최대 3개")