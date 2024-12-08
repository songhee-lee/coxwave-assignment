from pydantic import BaseSettings

class CommonSettings(BaseSettings) :
    class Config :
        env_file = ".env"

class LLMSettings(CommonSettings) :
    API_KEY : str
    GPT_MODEL : str

class PromptSettings(CommonSettings) :
    SYSTEM_PATH : str

    SYSTEM_PROMPT : str = None

    def __init__(self, **kwargs) :
        super().__init__(**kwargs)
        self.SYSTEM_PROMPT = self._read_file(self.SYSTEM_PATH) 

    def _read_file(self, path): 
        with open(path, "r", encoding="utf-8") as f: 
            return f.read()

class Settings(CommonSettings) :
    llm = LLMSettings()
    prompt = PromptSettings()

settings = Settings()