"""
    Unit tests for :mod:`ccai.bases.freezable`.
"""

import unittest

from ccai.bases.freezable import Freezable


class Settings(Freezable):

    def __init__(self, retries: int) -> None:
        super().__init__()
        self.retries = retries
        return


class TestFreezable(unittest.TestCase):

    def test_attributes_assignable_before_freeze(self) -> None:
        settings = Settings(retries=3)
        settings.retries = 5
        self.assertEqual(settings.retries, 5)
        return

    def test_assignment_after_freeze_raises(self) -> None:
        settings = Settings(retries=3)
        settings.freeze()
        with self.assertRaises(AttributeError):
            settings.retries = 5
        return

    def test_error_names_the_attribute(self) -> None:
        settings = Settings(retries=3)
        settings.freeze()
        with self.assertRaises(AttributeError) as caught:
            settings.timeout = 10
        self.assertIn("name=timeout", str(caught.exception))
        return

    def test_frozen_value_is_retained(self) -> None:
        settings = Settings(retries=3)
        settings.freeze()
        self.assertEqual(settings.retries, 3)
        return


if __name__ == "__main__":
    unittest.main()
