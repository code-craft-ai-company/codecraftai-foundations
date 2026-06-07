# Requirements

## Introduction

The `vpn-control-plane-protocol` feature defines `IVPNControlPlane` —
the Python `Protocol` for talking to a mesh-VPN *control plane API*
(`api.tailscale.com`, Twingate GraphQL). It is distinct from
`IVPNClient`, which talks to the *local daemon*. Splitting the two
protocols is the §1 architectural decision: control-plane operations
(mint auth keys, list devices, apply ACLs, delete devices) belong on
a separate surface so callers can compose them without dragging in a
running daemon, and so credentials for the API can be scoped
independently of the local installation.

The protocol takes credentials as typed objects (never bare tokens)
and uses Aspects on every call. Implementations live in
`codecraftai-interop/vpn/<provider>/<provider>controlplane.py` and are
built on `RestClientBase`.

**See Also:** [vpn-client-protocol](../vpn-client-protocol/design.md),
[tailscale-credentials](../../../codecraftai-credentials/specs/tailscale-credentials/design.md),
[twingate-credentials](../../../codecraftai-credentials/specs/twingate-credentials/design.md).

---

## Requirements

### Requirement 1: Mint a Short-Lived Auth Key

**User Story:** As the provisioning engine, I want to mint a
per-instance ephemeral, preauthorized auth key from an OAuth
credential, so that cloud-init payloads never contain a long-lived
static key (per §5 decision in the design plan).

#### Acceptance Criteria

1. THE SYSTEM SHALL declare `mint_authkey(reusable, ephemeral, tags,
   ttl_seconds, aspects) -> str` on `IVPNControlPlane`.
2. THE SYSTEM SHALL require `reusable: bool`, `ephemeral: bool`,
   `tags: List[str]`, `ttl_seconds: int` as keyword-only parameters.
3. WHEN the implementation rejects a TTL below the provider's minimum
   THE SYSTEM SHALL allow the implementation to raise.
4. WHERE the provider does not natively expose key minting (Twingate
   uses connector tokens issued differently) THE SYSTEM SHALL allow
   the implementation to raise `NotImplementedError` with a pointer
   to the provider-specific alternative.

---

### Requirement 2: List Registered Devices

**User Story:** As a landscape VPN-coordinator coupling, I want a
typed list of devices registered in the control plane, so I can
attach overlay addresses to landscape records.

#### Acceptance Criteria

1. THE SYSTEM SHALL declare
   `list_devices(aspects) -> List[VPNDeviceRecord]`.
2. THE SYSTEM SHALL define `VPNDeviceRecord` as a `@dataclass` with
   fields: `device_id: str`, `hostname: str`, `overlay_address:
   Optional[str]`, `tags: List[str]`, `os: Optional[str]`,
   `last_seen: Optional[str]`.
3. WHEN the control plane returns no devices THE SYSTEM SHALL allow
   implementations to return an empty list (no exception).

---

### Requirement 3: Delete a Device

**User Story:** As the destroy stage of the provisioning pipeline, I
want to de-register a device by id, so that tearing down a cloud
instance cleans up the control plane (especially for non-ephemeral
Twingate connectors).

#### Acceptance Criteria

1. THE SYSTEM SHALL declare
   `delete_device(device_id, aspects) -> None`.
2. WHEN the device is already absent THE SYSTEM SHALL allow
   implementations to treat the call as a no-op and return `None`
   (idempotent contract).
3. IF the credential lacks delete authority THEN THE SYSTEM SHALL
   propagate the provider's authorization exception.

---

### Requirement 4: Apply an ACL Document

**User Story:** As an operator, I want a single uniform entry point
to push an ACL fragment so tag-based access control can be set
post-apply.

#### Acceptance Criteria

1. THE SYSTEM SHALL declare
   `apply_acl(acl_doc, aspects) -> None` where `acl_doc: dict`.
2. WHERE the provider has no flat ACL doc (Twingate uses RBAC) THE
   SYSTEM SHALL allow implementations to raise
   `NotImplementedError` with a documented alternative API path.
3. THE SYSTEM SHALL document that the `acl_doc` shape is provider-
   specific and is not validated at the protocol layer.

---

### Requirement 5: Aspects on Every Behaviour-Bearing Call

**User Story:** As a caller, I want to control retries, timeouts,
and logging from the outside.

#### Acceptance Criteria

1. THE SYSTEM SHALL require `aspects: Aspects` (an `AspectsRest`
   subclass acceptable since `AspectsRest` IS-A `Aspects`) on every
   method.
2. IF an implementation adds `@retry` or any behaviour-modifying
   decorator to one of these methods THEN THE SYSTEM SHALL be
   considered non-conformant per the §8 usability commitments.

---

### Requirement 6: No Third-Party Imports

**User Story:** As a downstream consumer, I want the protocol module
to be dependency-free so it can be imported in low-tier packages.

#### Acceptance Criteria

1. THE SYSTEM SHALL import only `typing`, `dataclasses`, and
   `ccai.aspects.aspects` in `ivpncontrolplane.py`.
2. IF a future change introduces a third-party import to the
   protocol module THEN THE SYSTEM SHALL be considered non-
   conformant.
