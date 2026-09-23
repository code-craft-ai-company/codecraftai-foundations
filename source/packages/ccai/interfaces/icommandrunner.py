"""
    .. module:: icommandrunner
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Protocol for running commands and the result container they return.
"""

from typing import Protocol, Callable, Optional, Dict, List
from dataclasses import dataclass

__all__ = ["RunResult", "ICommandRunner"]


@dataclass
class RunResult:
    """
    Result of a command executed through an ICommandRunner.
    """
    exit_code: Optional[int]
    stdout: str
    stderr: str
    timed_out: bool = False


class ICommandRunner(Protocol):
    """
    Protocol defining the standard interface for executing commands across
    different system management domains.
    """
    def run(
        self,
        args: List[str],
        *,
        elevated: bool = False,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        stdin: Optional[str] = None,
        timeout: Optional[float] = None,
        on_output: Optional[Callable[[str], None]] = None,
        on_error: Optional[Callable[[str], None]] = None,
        capture_output: bool = True,
    ) -> RunResult:
        """
            Executes a command and returns a :class:`RunResult`.

            :param args: The command and its arguments as an argv list.
            :param elevated: When ``True`` the command is run with elevated privileges.
            :param cwd: The working directory for the command, or ``None`` for the runner default.
            :param env: The environment variables for the command, or ``None`` for the runner default.
            :param stdin: Text to send to the command on standard input, or ``None``.
            :param timeout: The maximum number of seconds to allow the command to run, or ``None``.
            :param on_output: Optional callback that receives standard output text.
            :param on_error: Optional callback that receives standard error text.
            :param capture_output: When ``True`` the output is captured into the returned result.

            :returns: The :class:`RunResult` with the exit code, output and timeout state of the command.
        """
