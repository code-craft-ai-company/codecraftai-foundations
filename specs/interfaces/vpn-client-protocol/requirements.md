# Requirements

## Introduction

The `vpn-client-protocol` feature introduces the `IVPNClient` Python `Protocol`
into `codecraftai-interfaces`. The protocol defines the host-side surface for a
mesh-VPN daemon (Tailscale `tailscaled`, Twingate connector) such that
sysman, interop, landscaping, and provisioning packages depend only on the
contract — never on a concrete vendor client. The protocol is a peer to the
existing `ICommandRunner` / `IFileOperator` protocols and follows the same
shape: a small, dependency-free interface plus a typed result dataclass.

All behaviour-bearing calls take an `Aspects` instance (Aspects pattern) so
callers control retries, timeouts, and logging from the outside. No
behaviour-modifying decorators appear on the protocol surface.

This spec defines the *contract only*. Concrete clients
(`vpn-tailscale-client`, `vpn-twingate-client`) live in `codecraftai-interop` and
implement this protocol.

**See Also:** [vpn-control-plane-protocol](../vpn-control-plane-protocol/design.md),
[address-plane-types](../address-plane-types/design.md).

---

## Requirements

### Requirement 1: Bring the Mesh-VPN Up on the Host

**User Story:** As an interop client implementer, I want a single
`bring_up` entry point that captures every parameter the daemon needs to join
the mesh, so that callers do not assemble vendor-specific argument lists.

#### Acceptance Criteria

1. THE SYSTEM SHALL declare `bring_up(authkey, hostname, advertise_tags, aspects)`
   on `IVPNClient` with `authkey: str`, `hostname: Optional[str]`,
   `advertise_tags: Optional[List[str]]`, and `aspects: Aspects`.
2. THE SYSTEM SHALL declare the return type as `VPNStatus`.
3. THE SYSTEM SHALL require every implementation to be callable with
   keyword-only arguments at the public boundary.
4. WHERE the underlying daemon does not support `advertise_tags` (e.g.
   Twingate connector) THE SYSTEM SHALL document that the implementation
   ignores the parameter rather than raise.
5. IF the daemon rejects the authkey THEN THE SYSTEM SHALL propagate an
   exception (no silent fallback); reclassification is the implementation's
   responsibility.

---

### Requirement 2: Bring the Mesh-VPN Down on the Host

**User Story:** As a teardown coordinator, I want a uniform `bring_down`
entry point so that destroy flows work the same on every vendor.

#### Acceptance Criteria

1. THE SYSTEM SHALL declare `bring_down(aspects)` returning `None`.
2. WHEN the daemon is already down THE SYSTEM SHALL allow implementations to
   return `None` without raising (idempotent semantics in the contract).
3. THE SYSTEM SHALL document that `bring_down` does not uninstall the daemon;
   uninstallation is owned by `codecraftai-sysman-*` per OS.

---

### Requirement 3: Query Current Status

**User Story:** As a landscape coordinator, I want a typed status query so I
can decide whether to re-attempt bring-up.

#### Acceptance Criteria

1. THE SYSTEM SHALL declare `status(aspects) -> VPNStatus`.
2. THE SYSTEM SHALL define `VPNStatus` as a `@dataclass` with fields:
   `connected: bool`, `backend_state: str`, `self_address: Optional[str]`,
   `hostname: Optional[str]`, `tags: List[str]`, `provider: str`.
3. WHEN the daemon is not installed THE SYSTEM SHALL allow implementations to
   raise; the contract does not require a "not installed" state.

---

### Requirement 4: Self Address Accessor

**User Story:** As an SSH connector, I want a plane-stable self-address
accessor so I can populate `DeviceAddressSet.overlay()` without parsing
status output.

#### Acceptance Criteria

1. THE SYSTEM SHALL declare `self_address() -> Optional[str]`.
2. WHERE the provider does not assign an overlay IP to each client (Twingate)
   THE SYSTEM SHALL allow `self_address()` to return `None` — this is the
   honest-fit decision from PLAN §3.
3. THE SYSTEM SHALL document that returning `None` is not an error.

---

### Requirement 5: Peer Address Enumeration

**User Story:** As a landscape VPN-coordinator coupling, I want a uniform
peer enumeration so I can attach overlay addresses to landscape devices.

#### Acceptance Criteria

1. THE SYSTEM SHALL declare `peer_addresses() -> Dict[str, str]` mapping
   peer hostname (or MagicDNS short name) to overlay IP.
2. WHERE the provider exposes no peer enumeration to clients THE SYSTEM SHALL
   allow implementations to return an empty dict.
3. THE SYSTEM SHALL NOT specify ordering on the returned dict.

---

### Requirement 6: Aspects on Every Behaviour-Bearing Call

**User Story:** As a caller, I want to control retries, timeouts, and
logging from the outside.

#### Acceptance Criteria

1. THE SYSTEM SHALL require `aspects: Aspects` as a parameter on every
   method that talks to the daemon (`bring_up`, `bring_down`, `status`).
2. IF an implementation adds `@retry` or any behaviour-modifying decorator to
   one of these methods THEN THE SYSTEM SHALL be considered non-conformant
   per the §8 usability commitments.
3. THE SYSTEM SHALL document `self_address` and `peer_addresses` as
   read-only accessors that may cache state populated by `status`; these do
   not require Aspects.
