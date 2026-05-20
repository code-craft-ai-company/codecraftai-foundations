# Design

## Overview

`IVPNControlPlane` is a Python `Protocol` placed under
`automojo-interfaces/source/packages/automojo/interfaces/ivpncontrolplane.py`.
It defines the API-side surface for a mesh-VPN control plane and the typed
`VPNDeviceRecord` dataclass that `list_devices` returns.

The protocol is intentionally narrow — it captures the four operations
the provisioning engine and landscape couplings need: mint an auth key,
enumerate devices, delete a device, apply an ACL. Provider-specific
operations (Twingate resource creation, Tailscale DNS policy) belong on
the concrete implementation, not on the protocol.

The split between `IVPNClient` (local daemon) and `IVPNControlPlane`
(remote API) is the §1 architectural decision in PLAN-VPN-AND-CLOUD-
PROVISIONING.md and is honoured strictly here: there is no overlap in
methods between the two protocols, and no implementation is required to
implement both.

**See Also:** [vpn-client-protocol](../vpn-client-protocol/design.md),
[address-plane-types](../address-plane-types/design.md),
[task-handle-protocol](../task-handle-protocol/design.md),
[restapigroup-enhancements](../../../automojo-restclient-base/specs/restapigroup-enhancements/design.md).

---

## Architecture

```
+---------------------------------+    uses     +-----------------------------+
| ProvisioningEngine              +------------>+ IVPNControlPlane (Protocol) |
|  (bootstrap VPN stage)          |             |  mint_authkey               |
+---------------------------------+             |  list_devices               |
                                                |  delete_device              |
+---------------------------------+    uses     |  apply_acl                  |
| VPNCoordinatorCoupling          +------------>+                             |
|  (landscape peer discovery)     |             +--------------+--------------+
+---------------------------------+                            |
                                                  implements   |
                       +-------------------------------+-------+-----------------+
                       |                                                         |
        +--------------v----------------+                    +-------------------v---+
        | TailscaleControlPlane         |                    | TwingateControlPlane  |
        |  RestClientBase against       |                    |  GraphQL on           |
        |  api.tailscale.com            |                    |  /api/graphql/        |
        |  TailscaleOAuthCredential or  |                    |  TwingateService-     |
        |  TailscaleAuthKeyCredential   |                    |  AccountCredential    |
        +-------------------------------+                    +-----------------------+
```

---

## Data Model

```python
from dataclasses import dataclass, field
from typing import List, Optional, Protocol

from automojo.aspects.aspects import Aspects


@dataclass
class VPNDeviceRecord:
    """
        A device entry returned by IVPNControlPlane.list_devices.

        :param device_id: Provider-assigned stable id.
        :param hostname: Hostname registered with the control plane.
        :param overlay_address: Overlay IP, or None for providers (Twingate)
            that do not assign one per client.
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


class IVPNControlPlane(Protocol):
    """
        Protocol for a mesh-VPN control plane API.
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
        ...

    def list_devices(self, *, aspects: Aspects) -> List[VPNDeviceRecord]:
        ...

    def delete_device(self, *, device_id: str, aspects: Aspects) -> None:
        ...

    def apply_acl(self, *, acl_doc: dict, aspects: Aspects) -> None:
        ...
```

---

## Module Layout

```
automojo-interfaces/source/packages/automojo/interfaces/
  ivpncontrolplane.py     <-- IVPNControlPlane + VPNDeviceRecord
  ivpnclient.py           (sibling spec)
  iaddressplane.py        (sibling spec)
  itaskhandle.py          (sibling spec)
```

---

## See Also

- [vpn-client-protocol](../vpn-client-protocol/design.md) — the local-
  daemon surface, peer to this protocol.
- [tailscale-credentials](../../../automojo-credentials/specs/tailscale-credentials/design.md)
  — `TailscaleOAuthCredential` is the canonical credential consumed by
  `mint_authkey`.
- [twingate-credentials](../../../automojo-credentials/specs/twingate-credentials/design.md).
- [task-handle-base](../../../automojo-restclient-base/specs/task-handle-base/design.md)
  — referenced for clients that surface long-running operations.

---

## Testing Strategy

The protocol is a typing artefact; no runtime computation lives here.

- **Import test.** `IVPNControlPlane`, `VPNDeviceRecord` import and are
  exported via `__all__`.
- **Protocol-shape test.** Each method's signature matches the design.
- **Conformance fixture.** A `MockVPNControlPlane` lives in the test root
  and is reused by `TailscaleControlPlane` / `TwingateControlPlane`
  conformance tests in `automojo-interop`.
- **No property tests required** — pure protocol, no computation.
