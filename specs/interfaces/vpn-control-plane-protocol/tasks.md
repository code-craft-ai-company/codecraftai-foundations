# Implementation Plan — VPN Control Plane Protocol

## Module and Models

- [x] 1. Create `automojo-interfaces/source/packages/automojo/interfaces/ivpncontrolplane.py`.
- [x] 2. Define `VPNDeviceRecord` dataclass with fields listed in the design.
- [x] 3. Define `IVPNControlPlane(Protocol)` with the four methods listed.
- [x] 4. Add module-level Sphinx docstring and per-method docstrings.

## IVPNControlPlane — To Implement

- [x] 5. Confirm every method uses keyword-only parameters.
- [x] 6. Confirm every method declares `aspects: Aspects`.
- [x] 7. Confirm no third-party imports — only `typing`, `dataclasses`,
  `automojo.aspects.aspects`.
- [x] 8. Add `__all__ = ["IVPNControlPlane", "VPNDeviceRecord"]`.
- [x] 9. Document `apply_acl` provider-specificity note in the docstring
  (Tailscale flat ACL vs Twingate RBAC).

## Testing

- [x] 10. `test_ivpncontrolplane_importable`.
- [x] 11. `test_ivpncontrolplane_is_protocol`.
- [x] 12. `test_ivpncontrolplane_signature_shape` — assert parameter names
  and types via `typing.get_type_hints`.
- [x] 13. Add `MockVPNControlPlane` conformance fixture in the test root.
- [x] 14. `test_vpndevicerecord_overlay_optional_for_twingate_pattern` —
  construct a record with `overlay_address=None` and verify no error.
