"""
    Unit tests for the :mod:`ccai.interfaces.iexcludefilter` module.
"""

import inspect
import unittest
from typing import Any, List
from unittest.mock import MagicMock

from ccai.interfaces.iexcludefilter import IExcludeFilter


class TestIExcludeFilterProtocol(unittest.TestCase):
    """
        Verify the contract shape of :class:`IExcludeFilter`.
    """

    def test_protocol_has_should_exclude(self) -> None:
        """
            ``should_exclude`` exists on the protocol.
        """
        has_method = hasattr(IExcludeFilter, "should_exclude")
        self.assertTrue(has_method)
        return

    def test_protocol_has_filter(self) -> None:
        """
            ``filter`` exists on the protocol.
        """
        has_method = hasattr(IExcludeFilter, "filter")
        self.assertTrue(has_method)
        return

    def test_should_exclude_signature(self) -> None:
        """
            ``should_exclude`` accepts an object and returns ``bool``.
        """
        sig = inspect.signature(IExcludeFilter.should_exclude)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "check_object"])
        self.assertEqual(params["check_object"].annotation, Any)
        self.assertEqual(sig.return_annotation, bool)
        return

    def test_filter_signature(self) -> None:
        """
            ``filter`` accepts a list and returns a list.
        """
        sig = inspect.signature(IExcludeFilter.filter)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "input_list"])
        self.assertEqual(params["input_list"].annotation, List[Any])
        self.assertEqual(sig.return_annotation, List[Any])
        return

    def test_filter_default_implementation_drops_matches(self) -> None:
        """
            The default ``filter`` drops items where ``should_exclude`` is ``True``.
        """
        class _DropOdds:
            def should_exclude(self, check_object: Any) -> bool:
                rtnval = (check_object % 2) == 1
                return rtnval
        flt = _DropOdds()
        result = IExcludeFilter.filter(flt, [1, 2, 3, 4, 5])
        self.assertEqual(result, [2, 4])
        return

    def test_filter_default_implementation_with_empty_list(self) -> None:
        """
            The default ``filter`` returns an empty list for an empty input.
        """
        class _DropAll:
            def should_exclude(self, check_object: Any) -> bool:
                return True
        flt = _DropAll()
        result = IExcludeFilter.filter(flt, [])
        self.assertEqual(result, [])
        return

    def test_mock_should_exclude_can_be_invoked(self) -> None:
        """
            A spec'd mock can stand in for the protocol.
        """
        mock_filter = MagicMock(spec=IExcludeFilter)
        mock_filter.should_exclude.return_value = False
        decision = mock_filter.should_exclude("anything")
        self.assertEqual(decision, False)
        return


if __name__ == "__main__":
    unittest.main()
