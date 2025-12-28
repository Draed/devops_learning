from fastapi import FastAPI, HTTPException
from typing import Dict, List

from app.models import Todo
from app.database import db

app = FastAPI()

@app.post("/todos/", response_model=Todo)
async def create_todo(todo: Todo) -> Todo:
    """Create a todo item.

    A server-generated identifier is returned.

    Args:
        item: Todo data (title and optional completed flag).

    Returns:
        The created ``Todo`` with a generated ``id``.
    """
    return await db.add_todo(todo)

@app.get("/todos/", response_model=Dict[int, Todo])
async def read_todos() -> List[Todo]:
    """Return all stored todo items."""
    return await db.list_todos()

@app.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int) -> Todo:
    """Fetch a todo by its identifier.

    Raises:
        HTTPException: 404 if the todo does not exist.
    """
    todo = await db.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.delete("/todos/{todo_id}", response_model=dict)
async def delete_todo(todo_id: int) -> str:
    """Remove a todo from the store.

    Raises:
        HTTPException: 404 if the todo does not exist.
    """
    success = await db.delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}
