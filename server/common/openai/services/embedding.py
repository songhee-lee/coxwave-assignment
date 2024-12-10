import openai
from typing import List

from server.common.openai.config import openai_settings
from server.common.openai.utils.tokenizer import openai_tokenizer

def text_to_embedding(text: str) -> List[float]:
    """
    텍스트 임베딩 생성
    text: 입력 텍스트
    """

    # text를 chunk로 분할
    chunks = openai_tokenizer.chunk_text(text, openai_settings.OPENAI_EMBEDDING_MAX_TOKENS)

    embeddings = []
    for chunk in chunks :
        embedding = openai.Embedding.create(
            input=chunk,
            model=openai_settings.OPENAI_EMBEDDING_MODEL
        )["data"][0]["embedding"]
        embeddings.append(embedding)
    
    averaged_embedding = [sum(x)/len(x) for x in zip(*embeddings)]
    return averaged_embedding