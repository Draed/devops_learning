"""
Todo app Model module
"""

from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
    """Model representing a single todo item.

    Attributes:
        id: Unique identifier for the todo. Assigned by the repository.
        title: Human-readable description of the task.
        completed: ``True`` if the task is finished, ``False`` otherwise.
            The default value is ``False``.
    """
    id: int
    title: str
    completed: Optional[bool] = False