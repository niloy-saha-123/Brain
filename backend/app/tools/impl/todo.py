"""Local todo tool (no approval)."""
from __future__ import annotations

from typing import Any, Dict

from pydantic import Field

from app.tools.base import ToolArgs, ToolResult


class TodoAddArgs(ToolArgs):
    text: str = Field(..., min_length=1)


class TodoListArgs(ToolArgs):
    pass


class TodoCompleteArgs(ToolArgs):
    todo_id: str = Field(..., min_length=1)


class TodoStore:
    def __init__(self) -> None:
        self._todos: Dict[str, Dict[str, Any]] = {}

    def add(self, text: str) -> Dict[str, Any]:
        todo_id = f"todo_{len(self._todos) + 1}"
        todo = {"todo_id": todo_id, "text": text, "status": "open"}
        self._todos[todo_id] = todo
        return todo

    def list(self):
        return list(self._todos.values())

    def complete(self, todo_id: str):
        if todo_id in self._todos:
            self._todos[todo_id]["status"] = "done"
            return self._todos[todo_id]
        raise KeyError(todo_id)


store = TodoStore()


class TodoAddTool:
    name = "todo.add"
    risk_level = "low"
    args_model = TodoAddArgs

    def requires_approval(self, args: TodoAddArgs, context: Dict[str, Any]) -> bool:
        return False

    async def execute(self, args: TodoAddArgs, context: Dict[str, Any]) -> ToolResult:
        todo = store.add(args.text)
        return ToolResult(ok=True, request={"text": args.text}, result={"todo": todo})


class TodoListTool:
    name = "todo.list"
    risk_level = "low"
    args_model = TodoListArgs

    def requires_approval(self, args: TodoListArgs, context: Dict[str, Any]) -> bool:
        return False

    async def execute(self, args: TodoListArgs, context: Dict[str, Any]) -> ToolResult:
        return ToolResult(ok=True, request={}, result={"todos": store.list()})


class TodoCompleteTool:
    name = "todo.complete"
    risk_level = "low"
    args_model = TodoCompleteArgs

    def requires_approval(self, args: TodoCompleteArgs, context: Dict[str, Any]) -> bool:
        return False

    async def execute(self, args: TodoCompleteArgs, context: Dict[str, Any]) -> ToolResult:
        todo = store.complete(args.todo_id)
        return ToolResult(ok=True, request={"todo_id": args.todo_id}, result={"todo": todo})
