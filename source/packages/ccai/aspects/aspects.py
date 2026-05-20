"""
    .. module:: aspects
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`Aspects` placeholder used by
                   contract-layer protocols across the ``automojo-*`` suite.

    The Aspects pattern packages behaviour-modifying parameters (retry counts,
    completion intervals, completion timeouts, logging hooks) into a single
    parameter so behaviour is controlled by callers rather than by decorators.

    This module declares the minimal :class:`Aspects` carrier required by the
    contract-layer protocols (``IVPNClient``, ``IVPNControlPlane``,
    ``ITaskHandle``). Concrete enrichments — ``AspectsRest``, ``AspectsCmd``,
    ``AspectsUPnP`` and similar — live in their respective implementation-tier
    packages and subclass :class:`Aspects`.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from dataclasses import dataclass
from typing import Optional


@dataclass
class Aspects:
    """
        Minimal carrier for behaviour-modifying parameters.

        :param completion_interval: Seconds between completion-poll iterations
            for callers that drive a synchronous wait loop.
        :param completion_timeout: Maximum seconds to wait for completion before
            the caller raises :class:`TimeoutError`.
        :param connection_timeout: Maximum seconds to wait for a single network
            attempt before reclassifying.
        :param max_attempts: Maximum number of attempts a caller is allowed to
            perform when reconciling against a remote system.
        :param logger_name: Optional logger name a caller can route logs into.
    """
    completion_interval: float = 10.0
    completion_timeout: float = 600.0
    connection_timeout: float = 60.0
    max_attempts: int = 1
    logger_name: Optional[str] = None


__all__ = ["Aspects"]
