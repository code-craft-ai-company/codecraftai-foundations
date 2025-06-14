"""
.. module:: iserializable
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the `ISerializable` protocol object which defines methods
               used to serialize and deserialize objects.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Dict, Protocol

class ISerializable(Protocol):
    """
        The :class:`ISerializable` interface defines methods for
        serializing and deserializing objects to and from dictionaries.
    """

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
            Creates an instance of the class from a dictionary representation.

            :param data: The dictionary containing the data for the object.

            :returns: A new instance of the class.
        """
        ...

    def as_dict(self) -> Dict[str, Any]:
        """
            Returns a dictionary representation of the object.

            :returns: The object serialized to a dictionary.
        """
        ...
