"""
    Unit tests for the :mod:`automojo.interfaces.itaskhandle` module.
"""

import dataclasses
import inspect
import typing
import unittest
from typing import List, Optional

from automojo.aspects.aspects import Aspects
from automojo.interfaces.itaskhandle import ITaskHandle, TaskResult, TaskState


class MockTaskHandle:
    """
        Programmable :class:`ITaskHandle` conformance fixture driving a
        scripted state sequence.
    """

    def __init__(self, *, task_id_value: str, states: Optional[List[TaskState]] = None) -> None:
        provided_states = states if states is not None else [
            TaskState.PENDING,
            TaskState.RUNNING,
            TaskState.SUCCEEDED,
        ]
        self._task_id_value: str = task_id_value
        self._states: List[TaskState] = provided_states
        self._cursor: int = 0
        self._last_observed: TaskState = self._states[0]
        return

    def _advance(self) -> TaskState:
        if self._cursor < len(self._states) - 1:
            self._cursor = self._cursor + 1
        rtnval = self._states[self._cursor]
        self._last_observed = rtnval
        return rtnval

    def wait(self, *, aspects: Aspects) -> TaskResult:
        terminal = {TaskState.SUCCEEDED, TaskState.FAILED, TaskState.CANCELLED}
        while True:
            state = self._advance()
            if state in terminal:
                break
        rtnval = TaskResult(task_id=self._task_id_value, state=state, progress=100)
        return rtnval

    def cancel(self, *, aspects: Aspects) -> None:
        terminal = {TaskState.SUCCEEDED, TaskState.FAILED, TaskState.CANCELLED}
        if self._last_observed not in terminal:
            self._last_observed = TaskState.CANCELLED
            self._states = self._states[: self._cursor + 1] + [TaskState.CANCELLED]
        return

    def is_done(self) -> bool:
        terminal = {TaskState.SUCCEEDED, TaskState.FAILED, TaskState.CANCELLED}
        rtnval = self._last_observed in terminal
        return rtnval

    def task_id(self) -> str:
        rtnval = self._task_id_value
        return rtnval


class TestTaskStateEnum(unittest.TestCase):
    """
        Verify the :class:`TaskState` enum.
    """

    def test_taskstate_members_present(self) -> None:
        """
            All five members exist with the expected ordinals.
        """
        self.assertEqual(int(TaskState.PENDING), 1)
        self.assertEqual(int(TaskState.RUNNING), 2)
        self.assertEqual(int(TaskState.SUCCEEDED), 3)
        self.assertEqual(int(TaskState.FAILED), 4)
        self.assertEqual(int(TaskState.CANCELLED), 5)
        self.assertEqual(len(list(TaskState)), 5)
        return


class TestTaskResultDataclass(unittest.TestCase):
    """
        Verify the shape and defaults of the :class:`TaskResult` dataclass.
    """

    def test_taskresult_is_dataclass(self) -> None:
        """
            Confirm :class:`TaskResult` is a dataclass.
        """
        is_dc = dataclasses.is_dataclass(TaskResult)
        self.assertTrue(is_dc)
        return

    def test_taskresult_field_names(self) -> None:
        """
            Confirm the dataclass declares the expected fields.
        """
        fields = dataclasses.fields(TaskResult)
        names = [f.name for f in fields]
        expected = ["task_id", "state", "progress", "error", "payload"]
        self.assertEqual(names, expected)
        return

    def test_taskresult_defaults(self) -> None:
        """
            Default values match the design.
        """
        result = TaskResult(task_id="t-1", state=TaskState.RUNNING)
        self.assertEqual(result.progress, 0)
        self.assertIsNone(result.error)
        self.assertIsNone(result.payload)
        return


class TestITaskHandleProtocol(unittest.TestCase):
    """
        Verify the contract shape of the :class:`ITaskHandle` protocol.
    """

    def test_itaskhandle_importable(self) -> None:
        """
            The protocol and its result types are importable.
        """
        self.assertIsNotNone(ITaskHandle)
        self.assertIsNotNone(TaskResult)
        self.assertIsNotNone(TaskState)
        return

    def test_itaskhandle_is_protocol(self) -> None:
        """
            ``ITaskHandle`` is a :class:`typing.Protocol`.
        """
        is_protocol = issubclass(ITaskHandle, typing.Protocol)
        self.assertTrue(is_protocol)
        return

    def test_wait_signature(self) -> None:
        """
            ``wait`` declares ``aspects`` (keyword-only) and returns
            :class:`TaskResult`.
        """
        sig = inspect.signature(ITaskHandle.wait)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "aspects"])
        self.assertEqual(params["aspects"].annotation, Aspects)
        self.assertEqual(params["aspects"].kind, inspect.Parameter.KEYWORD_ONLY)
        self.assertEqual(sig.return_annotation, TaskResult)
        return

    def test_cancel_signature(self) -> None:
        """
            ``cancel`` declares ``aspects`` (keyword-only) and returns
            ``None``.
        """
        sig = inspect.signature(ITaskHandle.cancel)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "aspects"])
        self.assertEqual(params["aspects"].annotation, Aspects)
        self.assertEqual(params["aspects"].kind, inspect.Parameter.KEYWORD_ONLY)
        self.assertEqual(sig.return_annotation, None)
        return

    def test_is_done_signature(self) -> None:
        """
            ``is_done`` takes no parameters beyond ``self`` and returns
            ``bool``.
        """
        sig = inspect.signature(ITaskHandle.is_done)
        self.assertEqual(list(sig.parameters.keys()), ["self"])
        self.assertEqual(sig.return_annotation, bool)
        return

    def test_task_id_signature(self) -> None:
        """
            ``task_id`` takes no parameters beyond ``self`` and returns
            ``str``.
        """
        sig = inspect.signature(ITaskHandle.task_id)
        self.assertEqual(list(sig.parameters.keys()), ["self"])
        self.assertEqual(sig.return_annotation, str)
        return

    def test_mock_implementation_satisfies_protocol(self) -> None:
        """
            The :class:`MockTaskHandle` fixture conforms to the protocol.
        """
        mock = MockTaskHandle(task_id_value="task-1")
        aspects = Aspects()
        result = mock.wait(aspects=aspects)
        self.assertEqual(result.task_id, "task-1")
        self.assertEqual(result.state, TaskState.SUCCEEDED)
        self.assertTrue(mock.is_done())
        return

    def test_mock_cancel_path(self) -> None:
        """
            Cancel before ``wait`` causes ``wait`` to observe a
            ``CANCELLED`` terminal state.
        """
        mock = MockTaskHandle(
            task_id_value="task-2",
            states=[TaskState.PENDING, TaskState.RUNNING, TaskState.RUNNING, TaskState.SUCCEEDED],
        )
        aspects = Aspects()
        mock.cancel(aspects=aspects)
        result = mock.wait(aspects=aspects)
        self.assertEqual(result.state, TaskState.CANCELLED)
        return


if __name__ == "__main__":
    unittest.main()
