from typing import Dict, List

import tiktoken


class OpenAITokenizer:
    def __init__(self, settings):
        self.settings = settings
        self.tokenizer = tiktoken.get_encoding(self.settings.OPENAI_TOKENIZER_MODEL)

    def chunk_text(self, text: str, max_tokens: int) -> Dict[str, List]:
        """
        텍스트를 토큰에 맞게 청킹하기
        """
        tokens = self.tokenizer.encode(text)

        chunks = []
        # text를 chunk로 분할
        for i in range(0, len(tokens), max_tokens):
            chunk_tokens = tokens[i : i + max_tokens]
            chunks.append(self.tokenizer.decode(chunk_tokens))

        return chunks

    def tokenize_text(self, text: str) -> int:
        tokens = self.tokenizer.encode(text)
        return len(tokens)
