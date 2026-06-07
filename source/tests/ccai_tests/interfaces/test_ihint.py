"""
    Unit tests for the :mod:`ccai.interfaces.ihint` module.
"""

import inspect
import unittest
from typing import Any
from unittest.mock import MagicMock

from ccai.interfaces.ihint import IHint


class TestIHintProtocol(unittest.TestCase):
    """
        Verify the contract shape of :class:`IHint`.
    """

    def test_protocol_has_get_hint(self) -> None:
        """
            ``get_hint`` exists on the protocol.
        """
        has_method = hasattr(IHint, "get_hint")
        self.assertTrue(has_method)
        return

    def test_protocol_has_matches(self) -> None:
        """
            ``matches`` exists on the protocol.
        """
        has_method = hasattr(IHint, "matches")
        self.assertTrue(has_method)
        return

    def test_get_hint_signature(self) -> None:
        """
            ``get_hint`` takes only ``self`` and returns ``str``.
        """
        sig = inspect.signature(IHint.get_hint)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self"])
        self.assertEqual(sig.return_annotation, str)
        return

    def test_matches_signature(self) -> None:
        """
            ``matches`` accepts an object and returns ``bool``.
        """
        sig = inspect.signature(IHint.matches)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "obj"])
        self.assertEqual(params["obj"].annotation, Any)
        self.assertEqual(sig.return_annotation, bool)
        return

    def test_mock_implementation_satisfies_shape(self) -> None:
        """
            A spec'd mock supplies the documented operations.
        """
        mock_hint = MagicMock(spec=IHint)
        mock_hint.get_hint.return_value = "h:1"
        mock_hint.matches.return_value = True
        self.assertEqual(mock_hint.get_hint(), "h:1")
        self.assertEqual(mock_hint.matches(object()), True)
        return


if __name__ == "__main__":
    unittest.main()
