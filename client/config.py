from pydantic_settings import BaseSettings

class Settings(BaseSettings) :
    API_HOST : str

    class Config :
        env_file = ".env"
        extra = "ignore"

settings = Settings()