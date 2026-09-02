"""
    .. module:: ivpncontrolplane
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`IVPNControlPlane` protocol
                   and the typed :class:`VPNDeviceRecord` dataclass returned
                   from :meth:`IVPNControlPlane.list_devices`.

    ``IVPNControlPlane`` is the API-side contract for talking to a mesh-VPN
    control plane (``api.tailscale.com``, Twingate GraphQL). It is separate
    from :class:`ccai.interfaces.ivpnclient.IVPNClient`, which talks to
    the local daemon.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from dataclasses import dataclass, field
from typing import List, Optional, Protocol, runtime_checkable

from ccai.aspects.aspects import Aspects


@dataclass
class VPNDeviceRecord:
    """
        A device entry returned by :meth:`IVPNControlPlane.list_devices`.

        :param device_id: Provider-assigned stable identifier.
        :param hostname: Hostname registered with the control plane.
        :param overlay_address: Overlay IP, or ``None`` for providers
            (Twingate) that do not assign one per client.
        :param tags: Tags currently attached to the device.
        :param os: OS string reported by the agent, when available.
        :param last_seen: ISO-8601 last-seen timestamp, when available.
    """
    device_id: str
    hostname: str
    overlay_address: Optional[str]
    tags: List[str] = field(default_factory=list)
    os: Optional[str] = None
    last_seen: Optional[str] = None


@runtime_checkable
class IVPNControlPlane(Protocol):
    """
        Protocol for a mesh-VPN control plane API.

        Implementations are built on ``RestClientBase`` (or a GraphQL
        equivalent) and consume typed credential objects from
        ``codecraftai-credentials``. All behaviour-bearing methods accept an
        :class:`Aspects` instance.
    """

    def mint_authkey(
        self,
        *,
        reusable: bool,
        ephemeral: bool,
        tags: List[str],
        ttl_seconds: int,
        aspects: Aspects,
    ) -> str:
        """
            Mint a short-lived authentication key.

            :param reusable: Whether the key may be reused across multiple
                node bring-ups.
            :param ephemeral: Whether the resulting node registration is
                ephemeral (auto-removed when the node goes offline).
            :param tags: Tags to bind to the issued key.
            :param ttl_seconds: Requested time-to-live in seconds.
            :param aspects: Behaviour control for the call.

            :returns: The minted authentication key string.

            :raises: Implementation-specific exception when ``ttl_seconds``
                is below the provider minimum.
            :raises: ``NotImplementedError`` when the provider has no
                native key-mint flow (Twingate).
        """
        ...

    def list_devices(self, *, aspects: Aspects) -> List[VPNDeviceRecord]:
        """
            Enumerate devices currently registered in the control plane.

            :param aspects: Behaviour control for the call.

            :returns: A list of :class:`VPNDeviceRecord` entries. An empty
                list is a valid response and is not an error.
        """
        ...

    def delete_device(self, *, device_id: str, aspects: Aspects) -> None:
        """
            De-register a device from the control plane.

            Implementations MUST treat the call as a no-op when the device
            is already absent (idempotent contract).

            :param device_id: Provider-assigned device identifier.
            :param aspects: Behaviour control for the call.

            :returns: ``None``.

            :raises: Provider-specific authorization exception when the
                credential lacks delete authority.
        """
        ...

    def apply_acl(self, *, acl_doc: dict, aspects: Aspects) -> None:
        """
            Apply an ACL document to the control plane.

            The ``acl_doc`` shape is provider-specific (Tailscale uses a
            flat JSON ACL document; Twingate uses RBAC) and is NOT
            validated at the protocol layer. Implementations whose
            provider has no flat ACL document MAY raise
            ``NotImplementedError`` and document the alternative API.

            :param acl_doc: Provider-specific ACL payload.
            :param aspects: Behaviour control for the call.

            :returns: ``None``.

            :raises: ``NotImplementedError`` when the provider has no flat
                ACL surface.
        """
        ...


__all__ = ["IVPNControlPlane", "VPNDeviceRecord"]
