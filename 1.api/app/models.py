from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
    id: int
    title: str
    completed: Optional[bool] = False
