from app.tools.impl.filesystem import FilesystemReadTool, FilesystemWriteTool
from app.tools.impl.terminal import TerminalTool
from app.tools.impl.git import GitStatusTool, GitDiffTool, GitCommitTool
from app.tools.impl.web import WebFetchTool
from app.tools.impl.todo import TodoAddTool, TodoListTool, TodoCompleteTool
from app.tools.impl.ide_patch import IDEPatchTool


def register_all_tools(registry) -> None:
    """Register all built-in tools into the given registry."""
    registry.register(FilesystemReadTool())
    registry.register(FilesystemWriteTool())
    registry.register(TerminalTool())
    registry.register(GitStatusTool())
    registry.register(GitDiffTool())
    registry.register(GitCommitTool())
    registry.register(WebFetchTool())
    registry.register(TodoAddTool())
    registry.register(TodoListTool())
    registry.register(TodoCompleteTool())
    registry.register(IDEPatchTool())


__all__ = [
    "FilesystemReadTool",
    "FilesystemWriteTool",
    "TerminalTool",
    "GitStatusTool",
    "GitDiffTool",
    "GitCommitTool",
    "WebFetchTool",
    "TodoAddTool",
    "TodoListTool",
    "TodoCompleteTool",
    "IDEPatchTool",
    "register_all_tools",
]
