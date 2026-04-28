"""
    Unit tests for the :mod:`automojo.interfaces.ibasiccredential` module.
"""

import inspect
import unittest
from unittest.mock import MagicMock

from automojo.interfaces.ibasiccredential import IBasicCredential


class TestIBasicCredentialProtocol(unittest.TestCase):
    """
        Verify the contract shape of the :class:`IBasicCredential` protocol.
    """

    def test_protocol_has_username_property(self) -> None:
        """
            ``username`` exists on the protocol class.
        """
        has_username = hasattr(IBasicCredential, "username")
        self.assertTrue(has_username)
        return

    def test_protocol_has_password_property(self) -> None:
        """
            ``password`` exists on the protocol class.
        """
        has_password = hasattr(IBasicCredential, "password")
        self.assertTrue(has_password)
        return

    def test_username_is_property(self) -> None:
        """
            ``username`` is declared as a ``property``.
        """
        username_attr = inspect.getattr_static(IBasicCredential, "username")
        is_property = isinstance(username_attr, property)
        self.assertTrue(is_property)
        return

    def test_password_is_property(self) -> None:
        """
            ``password`` is declared as a ``property``.
        """
        password_attr = inspect.getattr_static(IBasicCredential, "password")
        is_property = isinstance(password_attr, property)
        self.assertTrue(is_property)
        return

    def test_username_property_return_type(self) -> None:
        """
            The ``username`` property's getter is annotated to return ``str``.
        """
        username_attr = inspect.getattr_static(IBasicCredential, "username")
        sig = inspect.signature(username_attr.fget)
        self.assertEqual(sig.return_annotation, str)
        return

    def test_password_property_return_type(self) -> None:
        """
            The ``password`` property's getter is annotated to return ``str``.
        """
        password_attr = inspect.getattr_static(IBasicCredential, "password")
        sig = inspect.signature(password_attr.fget)
        self.assertEqual(sig.return_annotation, str)
        return

    def test_mock_implementation_satisfies_shape(self) -> None:
        """
            A spec'd mock supplies the property-like attributes.
        """
        mock_cred = MagicMock(spec=IBasicCredential)
        mock_cred.username = "alice"
        mock_cred.password = "secret"
        self.assertEqual(mock_cred.username, "alice")
        self.assertEqual(mock_cred.password, "secret")
        return


if __name__ == "__main__":
    unittest.main()
