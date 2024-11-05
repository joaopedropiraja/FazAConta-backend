from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4, uuid5

from lato import Command


class CreateTodo(Command):
    """This commands represents an intent to create a new todo"""

    todo_id: UUID = uuid4()
    title: str
    description: str = ""
    due_at: Optional[datetime] = None


class CompleteTodo(Command):
    """This commands represents an intent to complete an existing todo"""

    todo_id: UUID
