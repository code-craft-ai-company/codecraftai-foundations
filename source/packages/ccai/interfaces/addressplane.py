"""
    .. module:: addressplane
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the :class:`AddressPlane` enum, the
                   :class:`IDeviceAddressSet` protocol, and the small
                   :class:`DeviceAddressSetSnapshot` helper.

    The address-plane types formalise the multi-plane addressing model from
    section 1 of ``PLAN-VPN-AND-CLOUD-PROVISIONING.md``. A device may be
    reachable on a public, private, and overlay plane simultaneously; the
    legal way to ask "give me an address" is
    :meth:`IDeviceAddressSet.address_for`.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from dataclasses import dataclass
from enum import IntEnum
from typing import List, Optional, Protocol, runtime_checkable


class AddressPlane(IntEnum):
    """
        Named address planes on which a device may be reachable.

        ``PUBLIC`` is the default plane per the section 5 design decision
        in ``PLAN-VPN-AND-CLOUD-PROVISIONING.md`` ("Landscape default
        plane -> PUBLIC"). MagicDNS lookups resolve to ``OVERLAY``
        addresses and are not a plane of their own.

        - ``PUBLIC``  - routable on the public internet or via public DNS.
        - ``PRIVATE`` - reachable on the VPC or private network.
        - ``OVERLAY`` - reachable via a mesh-VPN overlay (Tailscale
          ``100.x.x.x``, Twingate connector-routed CIDR, MagicDNS short
          name).
    """
    PUBLIC = 1
    PRIVATE = 2
    OVERLAY = 3


@runtime_checkable
class IDeviceAddressSet(Protocol):
    """
        Read-only multi-address container for a device.

        Returned by landscape devices and consumed by every API that needs
        to choose a host on a specific plane. Implementations MUST honour
        the totality contract: any populated plane returns a non-empty
        string, any unpopulated plane returns ``None``.
    """

    def address_for(self, *, plane: AddressPlane) -> Optional[str]:
        """
            Return the address for a given plane.

            :param plane: The plane whose address is requested.

            :returns: The address string when populated, otherwise
                ``None``.
        """
        ...

    def has(self, *, plane: AddressPlane) -> bool:
        """
            Report whether a given plane is populated.

            :param plane: The plane to test.

            :returns: ``True`` when :meth:`address_for` would return a
                non-``None`` value for ``plane``, otherwise ``False``.
        """
        ...

    def planes(self) -> List[AddressPlane]:
        """
            Enumerate populated planes in ascending ordinal order.

            :returns: A list of populated :class:`AddressPlane` values in
                ascending ``IntEnum`` order.
        """
        ...

    def public(self) -> Optional[str]:
        """
            Convenience accessor for the public-plane address.

            :returns: The public address, or ``None`` when not populated.
        """
        ...

    def private(self) -> Optional[str]:
        """
            Convenience accessor for the private-plane address.

            :returns: The private address, or ``None`` when not populated.
        """
        ...

    def overlay(self) -> Optional[str]:
        """
            Convenience accessor for the overlay-plane address.

            :returns: The overlay address, or ``None`` when not populated.
        """
        ...


@dataclass(frozen=True)
class DeviceAddressSetSnapshot:
    """
        Minimal :class:`IDeviceAddressSet` implementation suitable for
        tests and for callers that already have all addresses in hand.

        Landscape coordinators should use the richer ``DeviceAddressSet``
        in ``automojo-landscaping``; this snapshot is a contract-layer
        convenience.

        :param public_address: The public-plane address, or ``None``.
        :param private_address: The private-plane address, or ``None``.
        :param overlay_address: The overlay-plane address, or ``None``.
    """
    public_address: Optional[str] = None
    private_address: Optional[str] = None
    overlay_address: Optional[str] = None

    def address_for(self, *, plane: AddressPlane) -> Optional[str]:
        """
            Return the address for a given plane.

            :param plane: The plane whose address is requested.

            :returns: The address string when populated, otherwise
                ``None``.
        """
        rtnval: Optional[str] = None
        if plane == AddressPlane.PUBLIC:
            rtnval = self.public_address
        elif plane == AddressPlane.PRIVATE:
            rtnval = self.private_address
        elif plane == AddressPlane.OVERLAY:
            rtnval = self.overlay_address
        return rtnval

    def has(self, *, plane: AddressPlane) -> bool:
        """
            Report whether a given plane is populated.

            :param plane: The plane to test.

            :returns: ``True`` when :meth:`address_for` would return a
                non-``None`` value for ``plane``, otherwise ``False``.
        """
        candidate = self.address_for(plane=plane)
        rtnval = candidate is not None
        return rtnval

    def planes(self) -> List[AddressPlane]:
        """
            Enumerate populated planes in ascending ordinal order.

            :returns: A list of populated :class:`AddressPlane` values in
                ascending ``IntEnum`` order.
        """
        ordered = (AddressPlane.PUBLIC, AddressPlane.PRIVATE, AddressPlane.OVERLAY)
        populated: List[AddressPlane] = []
        for plane in ordered:
            if self.has(plane=plane):
                populated.append(plane)
        return populated

    def public(self) -> Optional[str]:
        """
            Convenience accessor for the public-plane address.

            :returns: The public address, or ``None`` when not populated.
        """
        rtnval = self.public_address
        return rtnval

    def private(self) -> Optional[str]:
        """
            Convenience accessor for the private-plane address.

            :returns: The private address, or ``None`` when not populated.
        """
        rtnval = self.private_address
        return rtnval

    def overlay(self) -> Optional[str]:
        """
            Convenience accessor for the overlay-plane address.

            :returns: The overlay address, or ``None`` when not populated.
        """
        rtnval = self.overlay_address
        return rtnval


__all__ = ["AddressPlane", "IDeviceAddressSet", "DeviceAddressSetSnapshot"]
