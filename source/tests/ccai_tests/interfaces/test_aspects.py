"""
    Unit tests for the :mod:`ccai.aspects.aspects` module.

    Pins the contract-relevant default values of the :class:`Aspects` carrier,
    which are consumed by the IVPNClient / IVPNControlPlane / ITaskHandle
    protocols, and verifies that callers can override them.
"""

import dataclasses
import unittest
from typing import Optional

from ccai.aspects.aspects import Aspects


class TestAspectsDefaults(unittest.TestCase):
    """
        Verify the documented default values of :class:`Aspects`.
    """

    def test_default_values(self) -> None:
        """
            The defaults match the contract values consumed across the suite.

            :returns: ``None``
        """
        aspects = Aspects()
        self.assertEqual(aspects.completion_interval, 10.0)
        self.assertEqual(aspects.completion_timeout, 600.0)
        self.assertEqual(aspects.connection_timeout, 60.0)
        self.assertEqual(aspects.max_attempts, 1)
        self.assertIsNone(aspects.logger_name)
        return

    def test_is_dataclass(self) -> None:
        """
            :class:`Aspects` is a dataclass exposing the documented fields.

            :returns: ``None``
        """
        is_dataclass = dataclasses.is_dataclass(Aspects)
        self.assertTrue(is_dataclass)
        field_names = [f.name for f in dataclasses.fields(Aspects)]
        self.assertEqual(
            field_names,
            ["completion_interval", "completion_timeout", "connection_timeout", "max_attempts", "logger_name"]
        )
        return


class TestAspectsOverrides(unittest.TestCase):
    """
        Verify that callers can override the behaviour parameters.
    """

    def test_override_all_values(self) -> None:
        """
            Each field accepts a caller-supplied override.

            :returns: ``None``
        """
        aspects = Aspects(
            completion_interval=2.5,
            completion_timeout=30.0,
            connection_timeout=5.0,
            max_attempts=3,
            logger_name="ccai.test"
        )
        self.assertEqual(aspects.completion_interval, 2.5)
        self.assertEqual(aspects.completion_timeout, 30.0)
        self.assertEqual(aspects.connection_timeout, 5.0)
        self.assertEqual(aspects.max_attempts, 3)
        self.assertEqual(aspects.logger_name, "ccai.test")
        return

    def test_exports_only_aspects(self) -> None:
        """
            The module's public surface is exactly ``Aspects``.

            :returns: ``None``
        """
        import ccai.aspects.aspects as aspects_module
        self.assertEqual(aspects_module.__all__, ["Aspects"])
        return


if __name__ == "__main__":
    unittest.main()
