from typing import List

from openai import OpenAI

from server.llm.openai.config import OpenAISettings
from server.llm.openai.utils.tokenizer import OpenAITokenizer


class EmbeddingService:
    def __init__(self, api_key: str, settings: OpenAISettings, tokenizer: OpenAITokenizer):
        self.client = OpenAI(api_key=api_key)
        self.settings = settings
        self.tokenizer = tokenizer

    def text_to_embedding(self, text: str) -> List[float]:
        """
        텍스트 임베딩 생성
        text: 입력 텍스트
        """

        # text를 chunk로 분할
        chunks = self.tokenizer.chunk_text(
            text, self.settings.OPENAI_EMBEDDING_MAX_TOKENS
        )

        embeddings = []
        for chunk in chunks:
            response = self.client.embeddings.create(
                input=chunk, model=self.settings.OPENAI_EMBEDDING_MODEL
            )
            embedding = response.data[0].embedding
            embeddings.append(embedding)

        averaged_embedding = [sum(x) / len(x) for x in zip(*embeddings, strict=False)]
        return averaged_embedding
