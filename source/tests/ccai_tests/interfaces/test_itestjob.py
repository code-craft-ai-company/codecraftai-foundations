"""
    Unit tests for the :mod:`ccai.interfaces.itestjob` module.
"""

import inspect
import unittest
from typing import Any, List
from unittest.mock import MagicMock

from ccai.interfaces.itestjob import ITestJob


class TestITestJobProtocol(unittest.TestCase):
    """
        Verify the contract shape of :class:`ITestJob`.
    """

    def test_protocol_has_required_members(self) -> None:
        """
            All documented attributes/methods exist on the protocol.
        """
        expected = ["importerrors", "begin", "execute", "finalize", "query"]
        for name in expected:
            has_member = hasattr(ITestJob, name)
            self.assertTrue(has_member, "missing member '{}'".format(name))
        return

    def test_importerrors_is_property(self) -> None:
        """
            ``importerrors`` is declared as a ``property``.
        """
        attr = inspect.getattr_static(ITestJob, "importerrors")
        is_prop = isinstance(attr, property)
        self.assertTrue(is_prop)
        return

    def test_begin_signature(self) -> None:
        """
            ``begin`` takes only ``self`` and returns ``None``.
        """
        sig = inspect.signature(ITestJob.begin)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self"])
        self.assertEqual(sig.return_annotation, None)
        return

    def test_execute_signature(self) -> None:
        """
            ``execute`` takes only ``self`` and returns an ``int``.
        """
        sig = inspect.signature(ITestJob.execute)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self"])
        self.assertEqual(sig.return_annotation, int)
        return

    def test_finalize_signature(self) -> None:
        """
            ``finalize`` takes only ``self`` and returns ``None``.
        """
        sig = inspect.signature(ITestJob.finalize)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self"])
        self.assertEqual(sig.return_annotation, None)
        return

    def test_query_signature(self) -> None:
        """
            ``query`` accepts ``query`` and ``format`` and returns ``List[Any]``.
        """
        sig = inspect.signature(ITestJob.query)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "query", "format"])
        self.assertEqual(params["query"].annotation, str)
        self.assertEqual(params["format"].annotation, int)
        self.assertEqual(params["format"].default, 0)
        self.assertEqual(sig.return_annotation, List[Any])
        return

    def test_mock_implementation_satisfies_shape(self) -> None:
        """
            A spec'd mock can be invoked through the documented surface.
        """
        mock_job = MagicMock(spec=ITestJob)
        mock_job.execute.return_value = 0
        mock_job.query.return_value = []
        exit_code = mock_job.execute()
        self.assertEqual(exit_code, 0)
        results = mock_job.query("name=foo")
        self.assertEqual(results, [])
        return


if __name__ == "__main__":
    unittest.main()
