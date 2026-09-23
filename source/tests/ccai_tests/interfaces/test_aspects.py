"""
    Unit tests for the :mod:`ccai.aspects.aspects` module.

    Pins the contract-relevant default values of the :class:`Aspects` carrier,
    which are consumed by the IVPNClient / IVPNControlPlane / ITaskHandle
    protocols, and verifies that callers can override them.
"""

import dataclasses
import unittest

from ccai.aspects.aspects import Aspects
from ccai.bases.freezable import Freezable


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


class TestAspectsSemantics(unittest.TestCase):
    """
        Verify the identity, hashing and freezing semantics every subclass inherits.
    """

    def test_is_freezable(self) -> None:
        self.assertTrue(issubclass(Aspects, Freezable))
        return

    def test_compares_by_identity(self) -> None:
        first = Aspects()
        second = Aspects()
        self.assertNotEqual(first, second)
        self.assertEqual(first, first)
        return

    def test_is_hashable(self) -> None:
        aspects = Aspects()
        self.assertEqual(len({aspects, aspects}), 1)
        return

    def test_not_frozen_by_default(self) -> None:
        aspects = Aspects()
        aspects.max_attempts = 4
        self.assertEqual(aspects.max_attempts, 4)
        return

    def test_freeze_blocks_assignment_and_returns_self(self) -> None:
        aspects = Aspects()
        self.assertIs(aspects.freeze(), aspects)
        with self.assertRaises(AttributeError):
            aspects.max_attempts = 4
        return

    def test_subclass_adds_fields_then_freezes(self) -> None:

        class AspectsDomain(Aspects):
            def __init__(self, *, request_timeout: float = 30.0, **base: object) -> None:
                super().__init__(**base)
                self.request_timeout = request_timeout
                self.freeze()

        aspects = AspectsDomain(request_timeout=5.0, max_attempts=2)
        self.assertEqual(aspects.request_timeout, 5.0)
        self.assertEqual(aspects.max_attempts, 2)
        with self.assertRaises(AttributeError):
            aspects.request_timeout = 1.0
        return


if __name__ == "__main__":
    unittest.main()
