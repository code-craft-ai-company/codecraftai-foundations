"""
.. module:: waitmodel
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which contains objects used in conjunction with waiting.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import List, Optional, Protocol, Type

from types import TracebackType

import os
import threading

from datetime import datetime, timedelta

from ccai.waiting.constants import (
    TimeoutState,
    MSG_TEMPL_TIME_COMPONENTS,
)


class TimeoutContext:
    """
        The :class:`TimeoutContext` object is used to store the context used to track the timeout
        of a single operations or multiple consecutive operations.
    """
    def __init__(self, timeout: float, interval: float=0, delay: float=0, doevery: int=-1,
                 what_for: Optional[str]=None):
        """
            Initializes a :class:`TimeoutContext` instance.

            :param timeout: The maximum time in seconds allowed for the operation.
            :param interval: The delay in seconds between condition rechecks.
            :param delay: An optional starting delay before tracking begins.
            :param doevery: Indicates at what interval loops should run.
            :param what_for: A description of what the context is tracking.
        """
        self._timeout = timeout
        self._interval = interval
        self._delay = delay
        self._doevery = doevery
        self._what_for = what_for

        self._loop_counter = 0
        self._now_time = None
        self._start_time = None
        self._end_time = None
        self._final_attempt = False
        self._wait_state = TimeoutState.NotStarted
        return

    @property
    def completed(self) -> bool:
        """
            Indicates the wait was successfully completed.
        """
        return self._wait_state == TimeoutState.Completed

    @property
    def end_time(self) -> datetime:
        """
            Property to retrieve the current endtime
        """
        return self._end_time

    @property
    def delay(self) -> float:
        """
            Property for retrieving the delay value.
        """
        return self._delay

    @property
    def final_attempt(self) -> bool:
        """
            Property for retrieving the ``final_attempt`` marker and for monitoring and debugging
            calls to look at the final attempt marker.
        """
        return self._final_attempt

    @property
    def has_timed_out(self) -> bool:
        """
            Property indicating if the wait context reached its timeout while running.
        """
        htoval = False
        # Timing values are None until mark_begin()/mark_time() run; a read-only
        # accessor must not raise when queried before tracking has started.
        if self._now_time is not None and self._end_time is not None:
            htoval = self._wait_state != TimeoutState.Completed and self._now_time > self._end_time
        return htoval

    @property
    def interval(self) -> float:
        """
            Property for retrieving the interval value.
        """
        return self._interval

    @property
    def is_do_every_interval(self) -> bool:
        """
            Indicates if the current iteration satisfies the do-every interval.

            :returns: ``True`` if the loop counter is on the do-every interval.
        """
        dei = False
        if self._doevery > -1:
            dei = self._loop_counter % self._doevery == 0
        return dei

    @property
    def timeout(self) -> float:
        """
            Property for retrieving the timeout value.
        """
        return self._timeout

    @property
    def wait_state(self) -> TimeoutState:
        """
            Property to return the current wait state of the wait context.
        """
        return self._wait_state

    @property
    def what_for(self) -> str:
        """
            Property for retrieving the ``what_for`` value.
        """
        return self._what_for

    def continue_waiting(self) -> None:
        """
            Reset the wait context to a waiting state so we can continue waiting.
        """
        self._wait_state = TimeoutState.Running
        return

    def create_timeout(self, what_for: Optional[str]=None, detail: Optional[List[str]]=None,
                       mark_timeout: Optional[bool]=True) -> TimeoutError:
        """
            Helper method used to create detailed :class:`TimeoutError` exceptions
            that can be raised in the context of the looper method.
        """
        if what_for is None:
            what_for = self._what_for

        err_msg = self.format_timeout_message(what_for, detail=detail)
        err_inst = TimeoutError(err_msg)

        if mark_timeout:
            self.mark_timeout()

        return err_inst

    def extend_timeout(self, seconds: float) -> None:
        """
            Extend the timeout of the current wait context by the specified number of seconds.

            :param seconds: The time in seconds to extend the wait period.
        """
        self._end_time = self._end_time + timedelta(seconds=seconds)
        self._wait_state = TimeoutState.Running
        self._final_attempt = False
        return

    def format_timeout_message(self, what_for: str, detail: Optional[List[str]]=None) -> str:
        """
            Helper method used to create format a detailed error message for reporting a timeout
            condition.
        """
        diff_time = self._now_time - self._start_time
        err_msg_lines = [
            "Timeout waiting for {}:".format(what_for),
            MSG_TEMPL_TIME_COMPONENTS.format(self._timeout, self._start_time, self._end_time,
                                             self._now_time, diff_time),
        ]

        if detail is not None:
            err_msg_lines.extend(detail)

        err_msg = os.linesep.join(err_msg_lines)
        return err_msg

    def mark_begin(self) -> None:
        """
            Mark the wait context as running.
        """
        self._now_time = datetime.now()
        self._start_time = self._now_time
        self._end_time = self._start_time + timedelta(seconds=self._timeout)
        self._wait_state = TimeoutState.Running
        return

    def mark_complete(self) -> None:
        """
            Mark the wait context as complete.
        """
        self._wait_state = TimeoutState.Completed
        return

    def mark_final_attempt(self) -> None:
        """
            Mark the wait context as being in the final attempt condition.
        """
        self._final_attempt = True
        return

    def mark_time(self) -> None:
        """
            Called to mark the current time in the :class:`WaitContext` instance.
        """
        self._now_time = datetime.now()
        return

    def mark_timeout(self) -> None:
        """
            Called to mark the wait context as timed out.
        """
        self._wait_state = TimeoutState.TimedOut
        return

    def reduce_delay(self, secs: float) -> None:
        """
            Reduce the wait start delay.
        """
        if secs > self._delay:
            self._delay = 0
        else:
            self._delay = self._delay - secs
        return

    def should_continue(self) -> bool:
        """
            Indicates if a wait condition should continue based on time specifications and context.
        """
        self._now_time = datetime.now()
        self._loop_counter += 1

        scont = True

        if self._wait_state == TimeoutState.Completed:
            scont = False
        elif self._now_time > self._end_time:
            scont = False

        return scont



class WaitCallback(Protocol):
    """
        Protocol specifying the expected signature for wait callbacks.
    """

    def __call__(self, wctx: TimeoutContext, *args, **kwargs) -> bool:
        """
            This specifies a callable object that can accept variable arguments.
            The supplied :class:`WaitContext` instance exposes a ``final_attempt``
            attribute indicating if the invocation is the final attempt. The
            callback should return ``True`` when the expected condition is met.
        """

class WaitContext(TimeoutContext):
    """
        Place holder for differences that might arise between the base TimeoutContext and
        the WaitContext used for wait loops.
    """


class WaitGate:
    """
        Wrapper around :class:`threading.Event` that includes timeout metadata.
    """

    def __init__(self, gate: threading.Event, message: Optional[str]=None, timeout: Optional[float]=None,
                 timeout_args: Optional[list]=None):
        """
            Constructs a :class:`WaitGate` instance.

            :param gate: The underlying event object used for synchronization.
            :param message: Optional message to include in timeout errors.
            :param timeout: Optional timeout to use when waiting on the gate.
            :param timeout_args: Additional arguments used when formatting timeout errors.
        """
        self._gate = gate
        self._message = message
        self._timeout = timeout
        self._timeout_args = timeout_args
        return

    @property
    def gate(self) -> threading.Event:
        """
            The underlying :class:`threading.Event` object.
        """
        return self._gate

    @property
    def message(self) -> str:
        """
            Message to include in timeout errors.
        """
        return self._message

    @property
    def timeout(self) -> float:
        """
            The timeout in seconds used when waiting on the gate.
        """
        return self._timeout

    @property
    def timeout_args(self) -> list:
        """
            Additional arguments for formatting timeout errors.
        """
        return self._timeout_args

    def clear(self) -> None:
        """
            Clears the underlying gate.
        """
        self._gate.clear()
        return

    def is_set(self) -> bool:
        """
            Indicates if the underlying gate is set.

            :returns: ``True`` if the gate is set.
        """
        rtnval = self._gate.is_set()
        return rtnval

    def set(self) -> None:
        """
            Sets the underlying gate.
        """
        self._gate.set()
        return

    def _format_timeout_message(self, timeout: Optional[float]) -> str:
        """
            Builds the timeout error message from the gate's configured message
            and timeout arguments.

            :param timeout: The timeout value that elapsed.

            :returns: The assembled timeout error message.
        """
        errmsg_lines = []
        if self._message is not None and len(self._message) > 0:
            errmsg_lines.append(self._message)
        else:
            errmsg_lines.append("Timed out waiting for the gate to be set.")

        errmsg_lines.append(f"TIMEOUT: {timeout}")

        if self._timeout_args is not None and len(self._timeout_args) > 0:
            errmsg_lines.append("TIMEOUT ARGS:")
            for targ in self._timeout_args:
                errmsg_lines.append(f"    {targ}")

        errmsg = os.linesep.join(errmsg_lines)
        return errmsg

    def wait(self, timeout: Optional[float]=None, raise_timeout: bool=False) -> bool:
        """
            Waits for the gate to be set.

            :param timeout: Optional timeout override.
            :param raise_timeout: If ``True``, raise :class:`TimeoutError` when the gate is not set.

            :returns: ``True`` if the gate was set before the timeout.
            :raises: TimeoutError when ``raise_timeout`` is ``True`` and the gate is not set.
        """
        if timeout is None:
            timeout = self._timeout

        rtnval = self._gate.wait(timeout=timeout)
        if not rtnval:
            if raise_timeout:
                errmsg = self._format_timeout_message(timeout=timeout)
                raise TimeoutError(errmsg)

        return rtnval


class WaitingScope:
    """
        Context manager that clears all managed gates on entry so they can be
        coordinated as a group.  Call :meth:`wait` to block until every managed
        gate is set.  Exiting the scope does not implicitly wait — waiting is an
        explicit, caller-controlled action via :meth:`wait`.
    """

    def __init__(self, gates: List[WaitGate],):
        """
            Initializes the waiting scope.

            :param gates: The gates that will be coordinated.
        """
        self._gates = gates
        return

    def __enter__(self) -> "WaitingScope":
        """
            Clears all managed gates upon entering the scope.

            :returns: This :class:`WaitingScope` instance so it can be bound with
                ``with WaitingScope(gates) as scope``.
        """
        for gate in self._gates:
            gate.clear()
        return self

    def __exit__(self, ex_type: Optional[Type], ex_inst: Optional[BaseException], ex_tb: Optional[TracebackType]) -> None:
        """
            Called when exiting the waiting scope.  Waiting is explicit (call
            :meth:`wait`); exit performs no implicit blocking.
        """
        return

    def wait(self) -> None:
        """
            Waits for all managed gates to be set.
        """
        for gate in self._gates:
            gate.wait()

        return
