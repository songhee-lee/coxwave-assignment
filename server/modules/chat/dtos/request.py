from pydantic import BaseModel
from typing import List, Dict, Any

class ChatRequest(BaseModel):
    service : str
    taskId : str
    messages: List[Dict[str, Any]]