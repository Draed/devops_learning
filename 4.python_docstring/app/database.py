from typing import Optional, Dict

from app.models import Todo

class Database:
    def __init__(self):
        self.todos: Dict[int, Todo] = {}
        self.counter: int = 1

    async def add_todo(self, todo: Todo) -> Todo:
        todo.id = self.counter
        self.todos[self.counter] = todo
        self.counter += 1
        return todo

    async def get_todo(self, todo_id: int) -> Optional[Todo]:
        return self.todos.get(todo_id)

    async def list_todos(self) -> Dict[int, Todo]:
        return self.todos

    async def delete_todo(self, todo_id: int) -> bool:
        if todo_id in self.todos:
            del self.todos[todo_id]
            return True
        return False

db = Database()
