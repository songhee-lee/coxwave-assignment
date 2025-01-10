from pydantic import BaseModel


class ChatResponse(BaseModel):
    task_id: str
    generated_text: str | None = None
    error: str | None = None
