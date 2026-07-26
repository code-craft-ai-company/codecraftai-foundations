"""
    .. module:: schemavalidationerror
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`SchemaValidationError` schema exception.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []



class SchemaValidationError(ValueError):
    """
        Raised when a model object fails *shape* validation at construction time.

        Shape validation covers type membership, enum membership, parseable CIDRs,
        monotonic port ranges, non-empty required strings, and similar
        local-to-the-object checks.
    """
