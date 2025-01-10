from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


class ChatSettings(BaseSettings):
    SYSTEM_PROMPT_PATH: str = Field(env="SYSTEM_PROMPT_PATH")
    RAG_PROMPT_PATH: str = Field(env="RAG_PROMPT_PATH")

    @property
    def system_prompt(self) -> str:
        return self._read_file(self.SYSTEM_PROMPT_PATH)

    @property
    def rag_prompt(self) -> str:
        return self._read_file(self.RAG_PROMPT_PATH)

    # def __init__(self, **kwargs) :
    #     super().__init__(**kwargs)
    #     self.SYSTEM_PROMPT = self._read_file(self.SYSTEM_PROMPT_PATH)
    #     self.RAG_PROMPT = self._read_file(self.RAG_PROMPT_PATH)

    def _read_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    class Config:
        env_file = ".env"
        extra = "ignore"
