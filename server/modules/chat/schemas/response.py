from pydantic import BaseModel

class ChatResponse(BaseModel):
    taskId: str
    generated_text : str | None = None
    error : str | None = None