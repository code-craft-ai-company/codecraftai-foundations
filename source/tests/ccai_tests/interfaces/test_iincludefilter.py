"""
    Unit tests for the :mod:`ccai.interfaces.iincludefilter` module.
"""

import inspect
import unittest
from typing import Any, List
from unittest.mock import MagicMock

from ccai.interfaces.iincludefilter import IIncludeFilter


class TestIIncludeFilterProtocol(unittest.TestCase):
    """
        Verify the contract shape of :class:`IIncludeFilter`.
    """

    def test_protocol_has_should_include(self) -> None:
        """
            ``should_include`` exists on the protocol.
        """
        has_method = hasattr(IIncludeFilter, "should_include")
        self.assertTrue(has_method)
        return

    def test_protocol_has_filter(self) -> None:
        """
            ``filter`` exists on the protocol.
        """
        has_method = hasattr(IIncludeFilter, "filter")
        self.assertTrue(has_method)
        return

    def test_should_include_signature(self) -> None:
        """
            ``should_include`` accepts an object and returns ``bool``.
        """
        sig = inspect.signature(IIncludeFilter.should_include)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "check_object"])
        self.assertEqual(params["check_object"].annotation, Any)
        self.assertEqual(sig.return_annotation, bool)
        return

    def test_filter_signature(self) -> None:
        """
            ``filter`` accepts a list and returns a list.
        """
        sig = inspect.signature(IIncludeFilter.filter)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "input_list"])
        self.assertEqual(params["input_list"].annotation, List[Any])
        self.assertEqual(sig.return_annotation, List[Any])
        return

    def test_filter_default_implementation_includes_matches(self) -> None:
        """
            The protocol's default ``filter`` keeps items where ``should_include`` is ``True``.
        """
        class _OnlyEvens:
            def should_include(self, check_object: Any) -> bool:
                rtnval = (check_object % 2) == 0
                return rtnval
        flt = _OnlyEvens()
        result = IIncludeFilter.filter(flt, [1, 2, 3, 4, 5])
        self.assertEqual(result, [2, 4])
        return

    def test_filter_default_implementation_with_empty_list(self) -> None:
        """
            The default ``filter`` returns an empty list for an empty input.
        """
        class _AllIn:
            def should_include(self, check_object: Any) -> bool:
                return True
        flt = _AllIn()
        result = IIncludeFilter.filter(flt, [])
        self.assertEqual(result, [])
        return

    def test_mock_should_include_can_be_invoked(self) -> None:
        """
            A spec'd mock can stand in for the protocol.
        """
        mock_filter = MagicMock(spec=IIncludeFilter)
        mock_filter.should_include.return_value = True
        decision = mock_filter.should_include("anything")
        self.assertEqual(decision, True)
        return


if __name__ == "__main__":
    unittest.main()
