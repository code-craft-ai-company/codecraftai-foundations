"""
    .. module:: ibasiccredential
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the `IBasicCredential` protocol object which defines the properties
                   of a basic credential.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Protocol

class IBasicCredential(Protocol):
    """
        The :class:`IBasicCredential` interface defines the
        :pyattr:`username` and :pyattr:`password` attributes for
        credential objects.
    """

    @property
    def username(self) -> str:
        """
            The username associated with the credential
        """
    
    @property
    def password(self) -> str:
        """
            The password associated with the credential
        """
