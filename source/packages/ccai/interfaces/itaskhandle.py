"""
    .. module:: itaskhandle
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`ITaskHandle` protocol,
                   the typed :class:`TaskResult` dataclass, and the
                   :class:`TaskState` enum.

    ``ITaskHandle`` captures the synchronous-wait-on-async-API pattern the
    framework adopts uniformly per the section 6.6 decision in
    ``PLAN-VPN-AND-CLOUD-PROVISIONING.md``: every interop client that backs
    an async API returns a task handle whose poll loop is driven by
    :class:`Aspects` rather than by ``asyncio``.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from dataclasses import dataclass
from enum import IntEnum
from typing import Optional, Protocol, runtime_checkable

from ccai.aspects.aspects import Aspects


class TaskState(IntEnum):
    """
        Lifecycle state of an asynchronous remote task.

        - ``PENDING``   - accepted but not yet running.
        - ``RUNNING``   - currently executing.
        - ``SUCCEEDED`` - finished successfully (terminal).
        - ``FAILED``    - finished unsuccessfully (terminal).
        - ``CANCELLED`` - cancelled by caller (terminal).
    """
    PENDING = 1
    RUNNING = 2
    SUCCEEDED = 3
    FAILED = 4
    CANCELLED = 5


@dataclass
class TaskResult:
    """
        Final or in-progress snapshot of an async task's state.

        :param task_id: Provider-assigned task identifier.
        :param state: :class:`TaskState` value at observation time.
        :param progress: Integer percent complete (0-100) when known.
        :param error: Error string when ``state == TaskState.FAILED``,
            otherwise ``None``.
        :param payload: Provider-specific result payload, or ``None``.
    """
    task_id: str
    state: TaskState
    progress: int = 0
    error: Optional[str] = None
    payload: Optional[dict] = None


@runtime_checkable
class ITaskHandle(Protocol):
    """
        Protocol for a synchronous-poll handle on a remote async task.

        Implementations drive the poll loop using
        :attr:`Aspects.completion_interval` and
        :attr:`Aspects.completion_timeout`. The contract distinguishes
        "timed out waiting" from "task finished but failed" by raising
        ``TimeoutError`` for the former and returning a terminal
        :class:`TaskResult` for the latter.
    """

    def wait(self, *, aspects: Aspects) -> TaskResult:
        """
            Block until the task reaches a terminal state or the
            completion timeout elapses.

            :param aspects: Behaviour control. Implementations MUST drive
                the poll loop from
                :attr:`Aspects.completion_interval` and
                :attr:`Aspects.completion_timeout`.

            :returns: A :class:`TaskResult` whose ``state`` is one of
                :attr:`TaskState.SUCCEEDED`, :attr:`TaskState.FAILED`, or
                :attr:`TaskState.CANCELLED`.

            :raises: ``TimeoutError`` when
                :attr:`Aspects.completion_timeout` elapses without
                reaching a terminal state.
        """
        ...

    def cancel(self, *, aspects: Aspects) -> None:
        """
            Request cancellation of the in-flight task.

            Implementations MUST treat ``cancel`` as a no-op when the task
            is already in a terminal state.

            :param aspects: Behaviour control for the call.

            :returns: ``None``.

            :raises: ``NotImplementedError`` when the underlying API does
                not support cancellation.
        """
        ...

    def is_done(self) -> bool:
        """
            Report whether the task has reached a terminal state.

            :returns: ``True`` when the last observed state is terminal
                (``SUCCEEDED``, ``FAILED``, or ``CANCELLED``), otherwise
                ``False``.
        """
        ...

    def task_id(self) -> str:
        """
            Return the provider-assigned task identifier.

            :returns: The task identifier string.
        """
        ...


__all__ = ["ITaskHandle", "TaskResult", "TaskState"]
