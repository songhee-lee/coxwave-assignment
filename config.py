from pydantic import BaseSettings

class CommonSettings(BaseSettings) :
    class Config :
        env_file = ".env"

class LLMSettings(CommonSettings) :
    API_KEY : str
    GPT_MODEL : str

class Settings(CommonSettings) :
    llm = LLMSettings()

settings = Settings()