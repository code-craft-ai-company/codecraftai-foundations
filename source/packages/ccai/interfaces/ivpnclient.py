"""
    .. module:: ivpnclient
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`IVPNClient` protocol and the
                   typed :class:`VPNStatus` dataclass returned from its
                   ``bring_up`` and ``status`` calls.

    ``IVPNClient`` is the host-side contract for a mesh-VPN daemon
    (Tailscale ``tailscaled``, Twingate connector). Concrete implementations
    live under ``codecraftai-interop/vpn/<provider>/``; this module is the
    dependency-free contract those implementations honour.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from dataclasses import dataclass, field
from typing import Dict, List, Optional, Protocol, runtime_checkable

from ccai.aspects.aspects import Aspects


@dataclass
class VPNStatus:
    """
        Typed status snapshot returned by :meth:`IVPNClient.status` and
        :meth:`IVPNClient.bring_up`.

        :param connected: Whether the daemon is currently joined to the mesh.
        :param backend_state: Vendor-reported backend state token (e.g.
            ``"Running"``, ``"NeedsLogin"``, ``"Stopped"``).
        :param self_address: Overlay address assigned to this host, or
            ``None`` when the provider does not assign one per client
            (Twingate).
        :param hostname: Hostname registered with the control plane, or
            ``None``.
        :param tags: Tags currently advertised by this client.
        :param provider: Provider identifier, for example ``"tailscale"``
            or ``"twingate"``.
    """
    connected: bool
    backend_state: str
    self_address: Optional[str]
    hostname: Optional[str]
    tags: List[str] = field(default_factory=list)
    provider: str = ""


@runtime_checkable
class IVPNClient(Protocol):
    """
        Protocol for a host-side mesh-VPN daemon client.

        Implementations drive the local vendor daemon (``tailscaled``,
        ``twingate-connector``, etc.) through an injected command runner.
        All behaviour-bearing methods accept an :class:`Aspects` instance so
        callers control retries, timeouts, and logging from the outside.
    """

    def bring_up(
        self,
        *,
        authkey: str,
        hostname: Optional[str],
        advertise_tags: Optional[List[str]],
        aspects: Aspects,
    ) -> VPNStatus:
        """
            Bring the mesh-VPN daemon up and join the mesh.

            :param authkey: Vendor-issued authentication key.
            :param hostname: Hostname to register with the control plane, or
                ``None`` to defer to the daemon's default.
            :param advertise_tags: Tags to advertise on the mesh. Providers
                that do not support tags (Twingate) MAY ignore this
                parameter rather than raise.
            :param aspects: Behaviour control for the call.

            :returns: A :class:`VPNStatus` reflecting the post-bring-up
                state.

            :raises: Implementation-specific exceptions if the daemon
                rejects the auth key or fails to start.
        """

    def bring_down(self, *, aspects: Aspects) -> None:
        """
            Bring the mesh-VPN daemon down without uninstalling it.

            Implementations MAY treat ``bring_down`` as a no-op when the
            daemon is already down (idempotent semantics).

            :param aspects: Behaviour control for the call.

            :returns: ``None``.
        """

    def status(self, *, aspects: Aspects) -> VPNStatus:
        """
            Query the daemon for its current status.

            :param aspects: Behaviour control for the call.

            :returns: A :class:`VPNStatus` snapshot.

            :raises: Implementation-specific exception when the daemon is
                not installed.
        """

    def self_address(self) -> Optional[str]:
        """
            Return the overlay address assigned to this host, or ``None``
            when the provider does not assign one per client.

            This accessor is read-only and may return cached state
            populated by the most recent :meth:`status` or
            :meth:`bring_up`.

            :returns: An overlay address string, or ``None``.
        """

    def peer_addresses(self) -> Dict[str, str]:
        """
            Enumerate peers visible to this client.

            :returns: A mapping of peer hostname or MagicDNS short name to
                overlay IP. Implementations MAY return an empty dict when
                the provider exposes no peer enumeration.
        """


__all__ = ["IVPNClient", "VPNStatus"]
