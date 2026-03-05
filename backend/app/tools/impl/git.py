"""Git tools (status, diff, commit)."""
from __future__ import annotations

import subprocess
from typing import Any, Dict

from pydantic import Field

from app.tools.base import ToolArgs, ToolResult
from app.tools.policy import requires_approval


class GitStatusArgs(ToolArgs):
    path: str | None = Field(default=None, description="Repo path")


class GitDiffArgs(ToolArgs):
    path: str | None = Field(default=None, description="Repo path")
    staged: bool = Field(default=False)


class GitCommitArgs(ToolArgs):
    path: str | None = Field(default=None)
    message: str = Field(..., min_length=1)


def _run_git(args_list, cwd=None) -> subprocess.CompletedProcess:
    return subprocess.run(args_list, cwd=cwd, capture_output=True, text=True)


class GitStatusTool:
    name = "git.status"
    risk_level = "high"
    args_model = GitStatusArgs

    def requires_approval(self, args: GitStatusArgs, context: Dict[str, Any]) -> bool:
        return requires_approval(self.name, args.dict())

    async def execute(self, args: GitStatusArgs, context: Dict[str, Any]) -> ToolResult:
        proc = _run_git(["git", "status", "--short"], cwd=args.path)
        return ToolResult(
            ok=proc.returncode == 0,
            request={"path": args.path},
            result={"stdout": proc.stdout, "stderr": proc.stderr, "exit_code": proc.returncode},
        )


class GitDiffTool:
    name = "git.diff"
    risk_level = "high"
    args_model = GitDiffArgs

    def requires_approval(self, args: GitDiffArgs, context: Dict[str, Any]) -> bool:
        return requires_approval(self.name, args.dict())

    async def execute(self, args: GitDiffArgs, context: Dict[str, Any]) -> ToolResult:
        cmd = ["git", "diff"]
        if args.staged:
            cmd.append("--cached")
        proc = _run_git(cmd, cwd=args.path)
        return ToolResult(
            ok=proc.returncode == 0,
            request={"path": args.path, "staged": args.staged},
            result={"stdout": proc.stdout, "stderr": proc.stderr, "exit_code": proc.returncode},
        )


class GitCommitTool:
    name = "git.commit"
    risk_level = "high"
    args_model = GitCommitArgs

    def requires_approval(self, args: GitCommitArgs, context: Dict[str, Any]) -> bool:
        return requires_approval(self.name, args.dict())

    async def execute(self, args: GitCommitArgs, context: Dict[str, Any]) -> ToolResult:
        proc = _run_git(["git", "commit", "-am", args.message], cwd=args.path)
        return ToolResult(
            ok=proc.returncode == 0,
            request={"path": args.path, "message": args.message},
            result={"stdout": proc.stdout, "stderr": proc.stderr, "exit_code": proc.returncode},
        )
