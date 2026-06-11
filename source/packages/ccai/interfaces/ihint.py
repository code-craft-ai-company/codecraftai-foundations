"""
    .. module:: ihint
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Protocol for providing diagnostic hints to callers.
"""


from typing import Any, Protocol

__all__ = ["IHint"]


class IHint(Protocol):
    """
        The IHint interface is used to provide a common interface for performing a hint
        on objects.
    """

    def get_hint(self) -> str:
        """
            :returns: The hint string that can be used to identify the object.
        """

    def matches(self, obj: Any) -> bool:
        """
            :param obj: The object to check against the hint.

            :returns: True if the hint can be used to identify the object, False otherwise.
        """
