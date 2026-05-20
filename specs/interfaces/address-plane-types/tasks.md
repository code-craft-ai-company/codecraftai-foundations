# Implementation Plan — Address Plane Types

## Module and Models

- [x] 1. Create `automojo-interfaces/source/packages/automojo/interfaces/iaddressplane.py`.
- [x] 2. Define `AddressPlane(IntEnum)` with `PUBLIC=1`, `PRIVATE=2`,
  `OVERLAY=3`.
- [x] 3. Define `IDeviceAddressSet(Protocol)` with the six methods listed
  in the design.
- [x] 4. Define `DeviceAddressSetSnapshot(frozen=True)` dataclass
  implementing `IDeviceAddressSet`.
- [x] 5. Confirm no third-party imports — only `typing`, `enum`,
  `dataclasses`.
- [x] 6. Add `__all__ = ["AddressPlane", "IDeviceAddressSet",
  "DeviceAddressSetSnapshot"]`.

## AddressPlane / IDeviceAddressSet — To Implement

- [x] 7. Implement `DeviceAddressSetSnapshot.address_for` with explicit
  if/elif branches per the project standard (no compound returns).
- [x] 8. Implement `DeviceAddressSetSnapshot.has` in terms of
  `address_for`.
- [x] 9. Implement `DeviceAddressSetSnapshot.planes` returning planes in
  ascending `IntEnum` order.
- [x] 10. Implement the three convenience accessors (`public`,
  `private`, `overlay`).
- [x] 11. Sphinx-style docstrings on every public symbol.

## Testing

- [x] 12. `test_addressplane_members_present_and_ordered`.
- [x] 13. `test_snapshot_address_for_returns_populated_or_none`.
- [x] 14. `test_snapshot_planes_returns_ascending_populated_planes`.
- [x] 15. `test_snapshot_convenience_accessors_match_address_for`.
- [x] 16. Add `hypothesis` to the test-only dependency set.
- [x] 17. **Property P1 — Totality** (hypothesis).
- [x] 18. **Property P2 — `has`/`address_for` consistency** (hypothesis).
- [x] 19. **Property P3 — Idempotence under repeated lookup** (hypothesis).
- [x] 20. **Property P4 — Ascending ordering of `planes()`** (hypothesis).
- [x] 21. **Property P5 — Convenience-accessor equivalence** (hypothesis).
- [x] 22. **Property P6 — Round-trip construction** (hypothesis).
