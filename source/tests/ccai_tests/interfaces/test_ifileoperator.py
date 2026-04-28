"""
    Unit tests for the :mod:`automojo.interfaces.ifileoperator` module.
"""

import inspect
import unittest
from typing import List
from unittest.mock import MagicMock

from automojo.interfaces.ifileoperator import IFileOperator


class TestIFileOperatorProtocol(unittest.TestCase):
    """
        Verify the contract shape of the :class:`IFileOperator` protocol.
    """

    def test_protocol_has_required_methods(self) -> None:
        """
            ``IFileOperator`` exposes the documented methods.
        """
        expected_methods = [
            "write_text",
            "delete",
            "read_text",
            "list_dir",
            "exists",
        ]
        for name in expected_methods:
            has_method = hasattr(IFileOperator, name)
            self.assertTrue(has_method, "missing method '{}'".format(name))
        return

    def test_write_text_signature(self) -> None:
        """
            ``write_text`` accepts the documented parameters and returns ``None``.
        """
        sig = inspect.signature(IFileOperator.write_text)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "path", "content", "elevated"])
        self.assertEqual(params["path"].annotation, str)
        self.assertEqual(params["content"].annotation, str)
        self.assertEqual(params["elevated"].annotation, bool)
        self.assertEqual(params["elevated"].default, False)
        self.assertEqual(sig.return_annotation, None)
        return

    def test_delete_signature(self) -> None:
        """
            ``delete`` accepts a path and an elevated flag.
        """
        sig = inspect.signature(IFileOperator.delete)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "path", "elevated"])
        self.assertEqual(params["path"].annotation, str)
        self.assertEqual(params["elevated"].annotation, bool)
        self.assertEqual(params["elevated"].default, False)
        self.assertEqual(sig.return_annotation, None)
        return

    def test_read_text_signature(self) -> None:
        """
            ``read_text`` returns a ``str``.
        """
        sig = inspect.signature(IFileOperator.read_text)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "path", "elevated"])
        self.assertEqual(sig.return_annotation, str)
        self.assertEqual(params["elevated"].default, False)
        return

    def test_list_dir_signature(self) -> None:
        """
            ``list_dir`` returns a ``List[str]``.
        """
        sig = inspect.signature(IFileOperator.list_dir)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "path", "elevated"])
        self.assertEqual(sig.return_annotation, List[str])
        self.assertEqual(params["elevated"].default, False)
        return

    def test_exists_signature(self) -> None:
        """
            ``exists`` returns a ``bool``.
        """
        sig = inspect.signature(IFileOperator.exists)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "path", "elevated"])
        self.assertEqual(sig.return_annotation, bool)
        self.assertEqual(params["elevated"].default, False)
        return

    def test_mock_implementation_satisfies_shape(self) -> None:
        """
            A mock spec'd against :class:`IFileOperator` accepts the documented call shape.
        """
        mock_fileop = MagicMock(spec=IFileOperator)
        mock_fileop.exists.return_value = True
        mock_fileop.read_text.return_value = "content"
        mock_fileop.list_dir.return_value = ["a", "b"]

        exists_value = mock_fileop.exists("/tmp/x")
        self.assertEqual(exists_value, True)

        read_value = mock_fileop.read_text("/tmp/x")
        self.assertEqual(read_value, "content")

        list_value = mock_fileop.list_dir("/tmp")
        self.assertEqual(list_value, ["a", "b"])
        return


if __name__ == "__main__":
    unittest.main()
