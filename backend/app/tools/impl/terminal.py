"""Terminal command tool (approval required)."""
from __future__ import annotations

import asyncio
import shlex
import subprocess
from typing import Any, Dict

from pydantic import Field

from app.tools.base import ToolArgs, ToolResult
from app.tools.policy import requires_approval


class TerminalArgs(ToolArgs):
    cmd: str = Field(..., description="Command string to execute")
    cwd: str | None = Field(default=None, description="Working directory")
    timeout: int = Field(default=30, description="Timeout seconds")


class TerminalTool:
    name = "terminal.run"
    risk_level = "high"
    args_model = TerminalArgs

    def requires_approval(self, args: TerminalArgs, context: Dict[str, Any]) -> bool:
        return requires_approval(self.name, args.dict())

    async def execute(self, args: TerminalArgs, context: Dict[str, Any]) -> ToolResult:
        cmd_list = shlex.split(args.cmd)
        proc = await asyncio.create_subprocess_exec(
            *cmd_list,
            cwd=args.cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=args.timeout)
        except asyncio.TimeoutError:
            proc.kill()
            raise

        return ToolResult(
            ok=proc.returncode == 0,
            request={"cmd": args.cmd, "cwd": args.cwd},
            result={
                "stdout": stdout.decode(),
                "stderr": stderr.decode(),
                "exit_code": proc.returncode,
            },
        )
