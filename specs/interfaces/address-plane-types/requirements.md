# Requirements

## Introduction

The `address-plane-types` feature introduces the `AddressPlane` enum and
the `IDeviceAddressSet` protocol into `codecraftai-interfaces`. These types
formalise the §1 observation that a device in a mesh-VPN landscape is
reachable via *multiple* addresses on distinct planes — public, private,
and overlay — and replace the single `_host` string the framework
currently uses.

Per the §8 usability commitment "Addresses are a set, not a string,"
every API that accepts a host MUST eventually accept an
`IDeviceAddressSet`, and the legal way to ask "give me a reachable
address" is `addressset.address_for(plane)`.

This spec defines the *types only*. `DeviceAddressSet` (the concrete
class) lives in `codecraftai-landscaping`; `resolve_in_plane` (the helper
that consumes them) lives in `codecraftai-networking/address-plane-resolution`.

**Property tests are required (⊙)** because `address_for(plane)`'s
totality, fall-through ordering, and idempotence under repeated lookup
are computational invariants downstream code relies on.

**See Also:** [vpn-client-protocol](../vpn-client-protocol/design.md),
[address-plane-resolution](../../../codecraftai-networking/specs/address-plane-resolution/design.md).

---

## Requirements

### Requirement 1: Address Plane Enum

**User Story:** As a caller that needs to choose how to reach a host,
I want a finite, named set of address planes so I do not assemble
strings like `"overlay"`.

#### Acceptance Criteria

1. THE SYSTEM SHALL declare `AddressPlane(IntEnum)` with members
   `PUBLIC = 1`, `PRIVATE = 2`, `OVERLAY = 3`.
2. THE SYSTEM SHALL NOT include a `MAGIC_DNS` member — MagicDNS lookups
   resolve to `OVERLAY` addresses and are not a plane of their own.
3. THE SYSTEM SHALL document `PUBLIC` as the default plane consistent
   with §5 of the design plan ("Landscape default plane → `PUBLIC`").

---

### Requirement 2: Device Address Set Protocol

**User Story:** As an SSH/DNS/file-ops client, I want a typed
multi-address accessor so I can ask for the plane I need without
guessing the underlying schema.

#### Acceptance Criteria

1. THE SYSTEM SHALL declare `IDeviceAddressSet(Protocol)` with the
   following methods:
   - `address_for(plane) -> Optional[str]`
   - `has(plane) -> bool`
   - `planes() -> List[AddressPlane]`
2. THE SYSTEM SHALL declare convenience accessors `public() -> Optional[str]`,
   `private() -> Optional[str]`, `overlay() -> Optional[str]`.
3. WHEN a plane is not populated THE SYSTEM SHALL require
   `address_for(plane)` to return `None` (no exception, no empty string).
4. WHEN `address_for(plane)` is called repeatedly with the same `plane`
   THE SYSTEM SHALL return the same value (read-only snapshot semantics).

---

### Requirement 3: Address Set Construction Helper

**User Story:** As a test author and a landscape coordinator, I want a
small, in-protocol construction helper so callers do not need to
import a landscape class just to build a fixture.

#### Acceptance Criteria

1. THE SYSTEM SHALL provide a small `DeviceAddressSetSnapshot`
   dataclass implementing `IDeviceAddressSet` with `public`, `private`,
   and `overlay` as optional `str` fields.
2. THE SYSTEM SHALL document `DeviceAddressSetSnapshot` as suitable for
   tests and for callers that already have all three addresses in hand;
   landscape coordinators should use the richer `DeviceAddressSet` in
   `codecraftai-landscaping`.

---

### Requirement 4: No Third-Party Imports

**User Story:** As a downstream consumer, I want the types module to be
dependency-free.

#### Acceptance Criteria

1. THE SYSTEM SHALL import only `typing`, `enum`, and `dataclasses` in
   `iaddressplane.py`.

---

### Requirement 5: Plane Selection Totality

**User Story:** As a caller, I want a guarantee that asking for a plane
that is not populated does not crash.

#### Acceptance Criteria

1. THE SYSTEM SHALL require that for any `AddressPlane` value `p` and
   any `IDeviceAddressSet` instance `s`, `s.address_for(p)` returns
   either a non-empty `str` or `None`.
2. IF an implementation raises for an unpopulated plane THEN THE
   SYSTEM SHALL be considered non-conformant.
3. THE SYSTEM SHALL require `s.has(p) == (s.address_for(p) is not
   None)` as an invariant.

---

### Requirement 6: Plane Enumeration Stability

**User Story:** As a caller iterating planes, I want a deterministic
order so my logs and diagnostics are reproducible.

#### Acceptance Criteria

1. THE SYSTEM SHALL require `planes()` to return populated planes in
   ascending `IntEnum` order (`PUBLIC`, `PRIVATE`, `OVERLAY`).
