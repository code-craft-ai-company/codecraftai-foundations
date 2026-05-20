# Design

## Overview

`IVPNClient` is a Python `Protocol` placed under
`automojo-interfaces/source/packages/automojo/interfaces/ivpnclient.py`,
alongside the existing `ICommandRunner` and `IFileOperator` protocols. It
defines the host-side surface for a mesh-VPN daemon and the typed
`VPNStatus` result dataclass that bring-up and status return.

The protocol contains no behaviour, no imports of third-party packages, and
no I/O. Implementations live in `automojo-interop/vpn/<provider>/` and own
the vendor specifics; sysman, landscaping, and provisioning depend on this
protocol only.

The contract honours the §8 usability commitments:

- Named-only parameters at the public boundary.
- Aspects on every behaviour-bearing call (no `@retry`).
- Typed result dataclass (no dicts at the boundary).
- Honest fit: `self_address()` returns `Optional[str]` so providers without
  flat-mesh addressing (Twingate) are not forced to lie.

**See Also:** [vpn-control-plane-protocol](../vpn-control-plane-protocol/design.md),
[address-plane-types](../address-plane-types/design.md),
[vpn-overlay-profile](../../../automojo-networking/specs/vpn-overlay-profile/design.md).

---

## Architecture

```
+---------------------------+         +-------------------------+
|  Caller (sysman /         |  uses   |  IVPNClient (Protocol)  |
|  landscaping /            +-------->+  bring_up / bring_down  |
|  provisioning)            |         |  status / self_address  |
+---------------------------+         |  peer_addresses         |
                                      +-----------+-------------+
                                                  |
                                  implements      |
              +-----------------------------------+-----------------+
              |                                                     |
   +----------v------------+                          +-------------v---------+
   | TailscaleClient       |                          | TwingateClient        |
   | (automojo-interop/    |                          | (automojo-interop/    |
   |  vpn/tailscale/)      |                          |  vpn/twingate/)       |
   | drives `tailscale up` |                          | drives twingate CLI   |
   | via ICommandRunner    |                          | via ICommandRunner    |
   +-----------------------+                          +-----------------------+
```

---

## Data Model

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Protocol

from automojo.aspects.aspects import Aspects


@dataclass
class VPNStatus:
    """
        Typed status snapshot returned by IVPNClient.status / bring_up.

        :param connected: Whether the daemon is currently joined to the mesh.
        :param backend_state: Vendor-reported backend state token (e.g.
            "Running", "NeedsLogin", "Stopped").
        :param self_address: Overlay address assigned to this host, or None
            when the provider does not assign one (e.g. Twingate clients).
        :param hostname: Hostname registered with the control plane, or None.
        :param tags: Tags currently advertised by this client.
        :param provider: Provider id, e.g. "tailscale" / "twingate".
    """
    connected: bool
    backend_state: str
    self_address: Optional[str]
    hostname: Optional[str]
    tags: List[str] = field(default_factory=list)
    provider: str = ""


class IVPNClient(Protocol):
    """
        Protocol for a host-side mesh-VPN daemon client.
    """

    def bring_up(
        self,
        *,
        authkey: str,
        hostname: Optional[str],
        advertise_tags: Optional[List[str]],
        aspects: Aspects,
    ) -> VPNStatus:
        ...

    def bring_down(self, *, aspects: Aspects) -> None:
        ...

    def status(self, *, aspects: Aspects) -> VPNStatus:
        ...

    def self_address(self) -> Optional[str]:
        ...

    def peer_addresses(self) -> Dict[str, str]:
        ...
```

---

## Module Layout

```
automojo-interfaces/source/packages/automojo/interfaces/
  __init__.py
  ivpnclient.py            <-- IVPNClient + VPNStatus
  ivpncontrolplane.py      (see sibling spec)
  iaddressplane.py         (see address-plane-types spec)
  icommandrunner.py        (existing)
  ifileoperator.py         (existing)
  ibasiccredential.py      (existing)
```

`ivpnclient.py` MUST NOT import any third-party package. `Aspects` is
imported from `automojo.aspects.aspects`.

---

## See Also

- [vpn-control-plane-protocol](../vpn-control-plane-protocol/design.md) —
  the API-side protocol (mint auth keys, list devices, apply ACLs).
- [address-plane-types](../address-plane-types/design.md) — `AddressPlane`
  enum and `IDeviceAddressSet`; the surface that consumes
  `IVPNClient.self_address()` / `IVPNClient.peer_addresses()`.
- [tailscale-credentials](../../../automojo-credentials/specs/tailscale-credentials/design.md).
- [twingate-credentials](../../../automojo-credentials/specs/twingate-credentials/design.md).

---

## Testing Strategy

The protocol is a typing artefact — there is no runtime behaviour to test
beyond import and shape verification.

- **Import test.** Import `IVPNClient` and `VPNStatus`. Verify they exist
  and that `IVPNClient` is a `Protocol`.
- **Shape test.** Use `typing.get_type_hints` to verify each method's
  signature has the parameters and return type declared in this design.
- **Conformance fixture.** Provide a tiny `MockVPNClient` in the test root
  that satisfies the protocol. Concrete implementations
  (`TailscaleClient`, `TwingateClient`) reuse the same conformance test by
  parameterising over the implementation class.
- **No property tests required** — this spec carries no non-trivial
  computation; conformance is by typing only.
