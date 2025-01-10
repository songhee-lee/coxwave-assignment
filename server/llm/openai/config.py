from pydantic_settings import BaseSettings


class OpenAISettings(BaseSettings):
    OPENAI_API_KEY: str

    OPENAI_TOKENIZER_MODEL: str

    OPENAI_EMBEDDING_MODEL: str
    OPENAI_EMBEDDING_MAX_TOKENS: int = 8192

    OPENAI_LLM_MODEL: str
    OPENAI_LLM_MAX_TOKENS: int

    class Config:
        env_file = ".env"
        extra = "ignore"
