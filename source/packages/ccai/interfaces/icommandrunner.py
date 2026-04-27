from typing import Protocol, Callable, Optional, Dict, List
from dataclasses import dataclass

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
        ...
