"""
    Unit tests for the :mod:`automojo.interfaces.icommandrunner` module.
"""

import dataclasses
import inspect
import unittest
from typing import Callable, Dict, List, Optional
from unittest.mock import MagicMock

from automojo.interfaces.icommandrunner import ICommandRunner, RunResult


class TestRunResultDataclass(unittest.TestCase):
    """
        Verify the shape and defaults of the :class:`RunResult` dataclass.
    """

    def test_runresult_is_dataclass(self) -> None:
        """
            Confirm `RunResult` is a dataclass.
        """
        is_dc = dataclasses.is_dataclass(RunResult)
        self.assertTrue(is_dc)
        return

    def test_runresult_required_field_names(self) -> None:
        """
            Confirm the dataclass declares the expected field names in order.
        """
        fields = dataclasses.fields(RunResult)
        names = [f.name for f in fields]
        expected = ["exit_code", "stdout", "stderr", "timed_out"]
        self.assertEqual(names, expected)
        return

    def test_runresult_field_types(self) -> None:
        """
            Confirm declared type annotations on the fields.
        """
        annotations = RunResult.__annotations__
        self.assertEqual(annotations["exit_code"], Optional[int])
        self.assertEqual(annotations["stdout"], str)
        self.assertEqual(annotations["stderr"], str)
        self.assertEqual(annotations["timed_out"], bool)
        return

    def test_runresult_timed_out_default_false(self) -> None:
        """
            `timed_out` should default to ``False``.
        """
        result = RunResult(exit_code=0, stdout="", stderr="")
        self.assertEqual(result.timed_out, False)
        return

    def test_runresult_instantiation_full(self) -> None:
        """
            All four fields can be populated explicitly.
        """
        result = RunResult(
            exit_code=2,
            stdout="hello",
            stderr="oops",
            timed_out=True,
        )
        self.assertEqual(result.exit_code, 2)
        self.assertEqual(result.stdout, "hello")
        self.assertEqual(result.stderr, "oops")
        self.assertEqual(result.timed_out, True)
        return

    def test_runresult_replace(self) -> None:
        """
            :func:`dataclasses.replace` produces a new instance with the override applied.
        """
        original = RunResult(exit_code=0, stdout="a", stderr="b")
        replaced = dataclasses.replace(original, stdout="c")
        self.assertEqual(original.stdout, "a")
        self.assertEqual(replaced.stdout, "c")
        self.assertEqual(replaced.exit_code, 0)
        return


class TestICommandRunnerProtocol(unittest.TestCase):
    """
        Verify the contract shape of the :class:`ICommandRunner` protocol.
    """

    def test_protocol_has_run_method(self) -> None:
        """
            ``ICommandRunner`` exposes a ``run`` callable.
        """
        has_run = hasattr(ICommandRunner, "run")
        self.assertTrue(has_run)
        is_callable = callable(getattr(ICommandRunner, "run"))
        self.assertTrue(is_callable)
        return

    def test_run_signature_parameters(self) -> None:
        """
            ``run`` declares the documented parameter names.
        """
        sig = inspect.signature(ICommandRunner.run)
        param_names = list(sig.parameters.keys())
        expected = [
            "self",
            "args",
            "elevated",
            "cwd",
            "env",
            "stdin",
            "timeout",
            "on_output",
            "on_error",
            "capture_output",
        ]
        self.assertEqual(param_names, expected)
        return

    def test_run_signature_defaults(self) -> None:
        """
            ``run`` keyword-only parameters have the documented defaults.
        """
        sig = inspect.signature(ICommandRunner.run)
        params = sig.parameters
        self.assertEqual(params["elevated"].default, False)
        self.assertEqual(params["cwd"].default, None)
        self.assertEqual(params["env"].default, None)
        self.assertEqual(params["stdin"].default, None)
        self.assertEqual(params["timeout"].default, None)
        self.assertEqual(params["on_output"].default, None)
        self.assertEqual(params["on_error"].default, None)
        self.assertEqual(params["capture_output"].default, True)
        return

    def test_run_signature_return_annotation(self) -> None:
        """
            ``run`` returns a :class:`RunResult`.
        """
        sig = inspect.signature(ICommandRunner.run)
        self.assertEqual(sig.return_annotation, RunResult)
        return

    def test_run_signature_param_annotations(self) -> None:
        """
            Validate the parameter type annotations on ``run``.
        """
        sig = inspect.signature(ICommandRunner.run)
        params = sig.parameters
        self.assertEqual(params["args"].annotation, List[str])
        self.assertEqual(params["elevated"].annotation, bool)
        self.assertEqual(params["cwd"].annotation, Optional[str])
        self.assertEqual(params["env"].annotation, Optional[Dict[str, str]])
        self.assertEqual(params["stdin"].annotation, Optional[str])
        self.assertEqual(params["timeout"].annotation, Optional[float])
        self.assertEqual(params["on_output"].annotation, Optional[Callable[[str], None]])
        self.assertEqual(params["on_error"].annotation, Optional[Callable[[str], None]])
        self.assertEqual(params["capture_output"].annotation, bool)
        return

    def test_mock_implementation_satisfies_shape(self) -> None:
        """
            A mock with a ``run`` attribute is callable like the protocol.
        """
        mock_runner = MagicMock(spec=ICommandRunner)
        mock_runner.run.return_value = RunResult(exit_code=0, stdout="ok", stderr="")
        result = mock_runner.run(["/bin/true"])
        self.assertEqual(result.exit_code, 0)
        mock_runner.run.assert_called_once_with(["/bin/true"])
        return


if __name__ == "__main__":
    unittest.main()
