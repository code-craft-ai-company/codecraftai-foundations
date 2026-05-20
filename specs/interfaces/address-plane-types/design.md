# Design

## Overview

The `address-plane-types` module formalises the multi-plane addressing
model from §1 of `PLAN-VPN-AND-CLOUD-PROVISIONING.md`. It contributes
two artefacts to `automojo-interfaces`:

1. `AddressPlane` — a small `IntEnum` (`PUBLIC`, `PRIVATE`, `OVERLAY`).
2. `IDeviceAddressSet` — a `Protocol` describing the read surface of a
   multi-address container. A thin `DeviceAddressSetSnapshot` dataclass
   ships alongside as the test/construction convenience implementation.

These types are the precondition for every other plane-aware change
across the framework (`address-plane-resolution`,
`ssh-address-plane-awareness`, `device-address-set`,
`overlay-dns-resolver`). They carry no I/O, no third-party imports, and
no behaviour beyond constructor-stored state.

The §8 usability commitment "Addresses are a set, not a string" makes
this module load-bearing. The single-string `_host` field on landscape
devices is *removed*, not deprecated, once consumers adopt this surface.

**See Also:** [vpn-client-protocol](../vpn-client-protocol/design.md),
[address-plane-resolution](../../../automojo-networking/specs/address-plane-resolution/design.md),
[vpn-overlay-profile](../../../automojo-networking/specs/vpn-overlay-profile/design.md).

---

## Architecture

```
+------------------------------------------------------------------+
| automojo-interfaces                                              |
|                                                                  |
|  +---------------------+        +-----------------------------+  |
|  | AddressPlane        |        | IDeviceAddressSet           |  |
|  |   PUBLIC  = 1       |        |   address_for(plane)        |  |
|  |   PRIVATE = 2       +<-------+   has(plane)                |  |
|  |   OVERLAY = 3       |        |   planes()                  |  |
|  +---------------------+        |   public / private / overlay|  |
|                                 +--------------+--------------+  |
|                                                |                 |
|                                  +-------------v--------------+  |
|                                  | DeviceAddressSetSnapshot   |  |
|                                  |  (test/construction helper)|  |
|                                  +----------------------------+  |
+------------------------------------------------------------------+
                  ^                                         ^
                  | implements                              | consumes
   +--------------+---------------+         +---------------+----------------+
   | DeviceAddressSet             |         | resolve_in_plane(name, plane)  |
   | (automojo-landscaping)       |         | (automojo-networking)          |
   +------------------------------+         +--------------------------------+
```

---

## Data Model

```python
from dataclasses import dataclass
from enum import IntEnum
from typing import List, Optional, Protocol


class AddressPlane(IntEnum):
    """
        Named address planes on which a device may be reachable.

        PUBLIC  - routable on the public internet (or public DNS name).
        PRIVATE - reachable on the VPC / private network.
        OVERLAY - reachable via a mesh-VPN overlay (Tailscale 100.x.x.x,
                  Twingate connector-routed CIDR, MagicDNS short name).
    """
    PUBLIC = 1
    PRIVATE = 2
    OVERLAY = 3


class IDeviceAddressSet(Protocol):
    """
        Read-only multi-address container for a device. Returned by
        landscape devices and consumed by every API that needs to
        choose a host on a specific plane.
    """

    def address_for(self, *, plane: AddressPlane) -> Optional[str]:
        ...

    def has(self, *, plane: AddressPlane) -> bool:
        ...

    def planes(self) -> List[AddressPlane]:
        ...

    def public(self) -> Optional[str]:
        ...

    def private(self) -> Optional[str]:
        ...

    def overlay(self) -> Optional[str]:
        ...


@dataclass(frozen=True)
class DeviceAddressSetSnapshot:
    """
        Minimal IDeviceAddressSet implementation suitable for tests and
        for callers that already have all addresses in hand.
    """
    public_address: Optional[str] = None
    private_address: Optional[str] = None
    overlay_address: Optional[str] = None

    def address_for(self, *, plane: AddressPlane) -> Optional[str]:
        rtnval: Optional[str] = None
        if plane == AddressPlane.PUBLIC:
            rtnval = self.public_address
        elif plane == AddressPlane.PRIVATE:
            rtnval = self.private_address
        elif plane == AddressPlane.OVERLAY:
            rtnval = self.overlay_address
        return rtnval

    def has(self, *, plane: AddressPlane) -> bool:
        rtnval = self.address_for(plane=plane) is not None
        return rtnval

    def planes(self) -> List[AddressPlane]:
        populated: List[AddressPlane] = []
        for plane in (AddressPlane.PUBLIC, AddressPlane.PRIVATE, AddressPlane.OVERLAY):
            if self.has(plane=plane):
                populated.append(plane)
        return populated

    def public(self) -> Optional[str]:
        return self.public_address

    def private(self) -> Optional[str]:
        return self.private_address

    def overlay(self) -> Optional[str]:
        return self.overlay_address
```

All methods use keyword-only parameters at the public boundary per the
project standards.

---

## Module Layout

```
automojo-interfaces/source/packages/automojo/interfaces/
  iaddressplane.py    <-- AddressPlane, IDeviceAddressSet,
                          DeviceAddressSetSnapshot
```

---

## See Also

- [vpn-client-protocol](../vpn-client-protocol/design.md) — supplies
  `IVPNClient.self_address()` / `peer_addresses()` consumed by the
  landscape implementation of `IDeviceAddressSet`.
- [address-plane-resolution](../../../automojo-networking/specs/address-plane-resolution/design.md)
  — `resolve_in_plane(name, plane, aspects)` is the canonical caller.
- [interface-class-vpn-overlay](../../../automojo-networking/specs/interface-class-vpn-overlay/design.md)
  — `InterfaceClass.VPN_OVERLAY` is the per-NIC equivalent of
  `AddressPlane.OVERLAY` and pairs with this enum at the descriptor
  level.

---

## Testing Strategy

This feature is marked **⊙** — property tests are required.

### Example-based tests

- `test_addressplane_members_present_and_ordered` — exactly three
  members in ascending int order.
- `test_snapshot_address_for_returns_populated_or_none`.
- `test_snapshot_planes_returns_ascending_populated_planes`.
- `test_snapshot_convenience_accessors_match_address_for`.

### Property-based tests (hypothesis)

Generators:

- `plane_strategy = sampled_from(list(AddressPlane))`
- `optional_addr = one_of(none(), text(min_size=1, max_size=64))`

Properties:

- **P1 — Totality.** For any tuple of three `optional_addr` and any
  `AddressPlane p`, `DeviceAddressSetSnapshot(*tuple).address_for(plane=p)`
  returns either `None` or a `str` (never raises).
- **P2 — `has`/`address_for` consistency.** For any snapshot `s` and any
  `p`, `s.has(plane=p) == (s.address_for(plane=p) is not None)`.
- **P3 — Idempotence.** For any snapshot `s` and any `p`,
  `s.address_for(plane=p) == s.address_for(plane=p)` across repeated
  invocations (read-only snapshot semantics).
- **P4 — Ordering.** For any snapshot `s`, `s.planes()` is a strictly
  ascending sequence drawn from `AddressPlane` ordinals.
- **P5 — Convenience equivalence.** For any snapshot `s` and any
  `p`, the convenience accessor (`public()`, `private()`, `overlay()`)
  returns the same value as `address_for(plane=p)`.
- **P6 — Round-trip.** For any `(a, b, c)` of optional address strings,
  constructing `DeviceAddressSetSnapshot(a, b, c)` and then querying
  each plane yields back `(a, b, c)` in order.

All property tests live in the same `unittest`-shaped harness used
elsewhere in the repository; `hypothesis` is added to the test-only
dependency set.
