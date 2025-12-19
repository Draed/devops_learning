from fastapi import FastAPI, HTTPException
from typing import Dict

from models import Todo
from database import db

app = FastAPI()

@app.post("/todos/", response_model=Todo)
async def create_todo(todo: Todo):
    return await db.add_todo(todo)

@app.get("/todos/", response_model=Dict[int, Todo])
async def read_todos():
    return await db.list_todos()

@app.get("/todos/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int):
    todo = await db.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.delete("/todos/{todo_id}", response_model=dict)
async def delete_todo(todo_id: int):
    success = await db.delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}
