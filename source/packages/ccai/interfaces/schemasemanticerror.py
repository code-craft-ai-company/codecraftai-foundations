"""
    .. module:: schemasemanticerror
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`SchemaSemanticError` schema exception.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []

from ccai.errors.exceptions import SemanticError


class SchemaSemanticError(SemanticError):
    """
        Raised when a model object fails *cross-resource* semantic validation.

        Semantic validation includes subnet-in-network containment, sibling-subnet
        non-overlap, accelerator support on the chosen venue, and other invariants
        that require looking across more than one object.

        This derives from :class:`ccai.errors.exceptions.SemanticError` (which
        is rooted at ``BaseException``) so that an ordinary ``except Exception`` or
        ``except RuntimeError`` does NOT silently swallow a semantic-validation
        failure. Per the project coding standards, ``SemanticError`` must never be
        caught -- it always bubbles.
    """
