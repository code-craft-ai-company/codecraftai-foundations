"""
    Unit tests for the :mod:`automojo.interfaces.iserializable` module.
"""

import inspect
import unittest
from typing import Any, Dict
from unittest.mock import MagicMock

from automojo.interfaces.iserializable import ISerializable


class TestISerializableProtocol(unittest.TestCase):
    """
        Verify the contract shape of :class:`ISerializable`.
    """

    def test_protocol_has_from_dict(self) -> None:
        """
            ``from_dict`` exists on the protocol.
        """
        has_method = hasattr(ISerializable, "from_dict")
        self.assertTrue(has_method)
        return

    def test_protocol_has_as_dict(self) -> None:
        """
            ``as_dict`` exists on the protocol.
        """
        has_method = hasattr(ISerializable, "as_dict")
        self.assertTrue(has_method)
        return

    def test_from_dict_is_classmethod(self) -> None:
        """
            ``from_dict`` is declared as a classmethod.
        """
        attr = inspect.getattr_static(ISerializable, "from_dict")
        is_cm = isinstance(attr, classmethod)
        self.assertTrue(is_cm)
        return

    def test_from_dict_signature(self) -> None:
        """
            ``from_dict`` accepts ``cls`` and ``data``.
        """
        attr = inspect.getattr_static(ISerializable, "from_dict")
        sig = inspect.signature(attr.__func__)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["cls", "data"])
        self.assertEqual(params["data"].annotation, Dict[str, Any])
        return

    def test_as_dict_signature(self) -> None:
        """
            ``as_dict`` returns a ``Dict[str, Any]``.
        """
        sig = inspect.signature(ISerializable.as_dict)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self"])
        self.assertEqual(sig.return_annotation, Dict[str, Any])
        return

    def test_mock_implementation_satisfies_shape(self) -> None:
        """
            A spec'd mock supports ``as_dict`` and ``from_dict``.
        """
        mock_serializable = MagicMock(spec=ISerializable)
        mock_serializable.as_dict.return_value = {"x": 1}
        result = mock_serializable.as_dict()
        self.assertEqual(result, {"x": 1})
        return


if __name__ == "__main__":
    unittest.main()
