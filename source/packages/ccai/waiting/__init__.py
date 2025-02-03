

"""
.. module:: waiting
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module which exports the public elements of the 'waiting' package.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []

from automojo.waiting.constants import (
    TimeoutState,
    DEFAULT_WAIT_DELAY,
    DEFAULT_WAIT_INTERVAL,
    DEFAULT_WAIT_TIMEOUT,
    MSG_TEMPL_TIME_COMPONENTS
)

from automojo.waiting.waitfunction import wait_for_it

from automojo.waiting.waitmodel import (
    TimeoutContext,
    WaitContext,
    WaitGate,
    WaitingScope,
    WaitCallback
)

__all__ = [
    "DEFAULT_WAIT_DELAY",
    "DEFAULT_WAIT_INTERVAL",
    "DEFAULT_WAIT_TIMEOUT",
    "MSG_TEMPL_TIME_COMPONENTS",
    "TimeoutContext",
    "TimeoutState",
    "WaitCallback",
    "WaitContext",
    "WaitGate",
    "WaitingScope",
    "wait_for_it"
]