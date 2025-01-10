from typing import Any, Dict, List

from pydantic import BaseModel


class ChatRequest(BaseModel):
    service: str
    task_id: str
    messages: List[Dict[str, Any]]
