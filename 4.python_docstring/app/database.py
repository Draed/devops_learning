"""
Todo app database management module
"""
from typing import Optional, Dict

from app.models import Todo

class Database:
    """
    class that manage Todo ORM in database 
    """
    def __init__(self):
        """
        Initialize a Database object for todo application, in order to manage todo ORM.
        """
        self.todos: Dict[int, Todo] = {}
        """python dictionnary of todo objects"""
        self.counter: int = 1
        """counter that represent the id / number (as integer) of todo in the database"""


    async def add_todo(self, todo: Todo) -> Todo:
        """Add a new ``Todo`` to the repository.

        The method assigns a unique ``id`` to ``todo`` using the internal
        counter, stores the object, increments the counter, and returns the
        stored instance.

        Args:
            todo: The ``Todo`` instance to store. Its ``id`` attribute will be
                overwritten with the newly assigned identifier.

        Returns:
            The same ``Todo`` instance after its ``id`` has been set.
        """
        todo.id = self.counter
        self.todos[self.counter] = todo
        self.counter += 1
        return todo

    async def get_todo(self, todo_id: int) -> Optional[Todo]:
        """Retrieve a ``Todo`` by its identifier.

        Args:
            todo_id: The integer ID of the desired ``Todo``.

        Returns:
            The matching ``Todo`` if it exists; otherwise ``None``.
        """
        return self.todos.get(todo_id)

    async def list_todos(self) -> Dict[int, Todo]:
        """Return the full mapping of stored todos.

        Returns:
            A dictionary where keys are todo IDs and values are ``Todo``
            instances.
        """
        return self.todos

    async def delete_todo(self, todo_id: int) -> bool:
        """Remove a ``Todo`` from the repository.

        Args:
            todo_id: The integer ID of the ``Todo`` to delete.

        Returns:
            ``True`` if the ``Todo`` was found and deleted; ``False`` otherwise.
        """
        if todo_id in self.todos:
            del self.todos[todo_id]
            return True
        return False


