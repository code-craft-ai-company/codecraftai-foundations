# Implementation Plan — VPN Client Protocol

## Module and Models

- [x] 1. Create `automojo-interfaces/source/packages/automojo/interfaces/ivpnclient.py`.
- [x] 2. Define `VPNStatus` dataclass with the fields listed in the design
  (`connected`, `backend_state`, `self_address`, `hostname`, `tags`, `provider`).
- [x] 3. Define `IVPNClient(Protocol)` with the five methods listed in the
  design.
- [x] 4. Add module-level Sphinx docstring and per-method Sphinx-style
  docstrings (no implementation bodies).

## IVPNClient — To Implement

- [x] 5. Confirm every method uses keyword-only parameters at the public
  boundary (PEP 3102 `*`).
- [x] 6. Confirm `bring_up`, `bring_down`, and `status` declare
  `aspects: Aspects` and that `self_address` / `peer_addresses` do not.
- [x] 7. Confirm no third-party imports — only `typing`, `dataclasses`, and
  `automojo.aspects.aspects`.
- [x] 8. Add `__all__ = ["IVPNClient", "VPNStatus"]`.

## Testing

- [x] 9. Add `test_ivpnclient_importable` — import succeeds and exports the
  expected names.
- [x] 10. Add `test_ivpnclient_is_protocol` — `IVPNClient` is a `Protocol`.
- [x] 11. Add `test_ivpnclient_signature_shape` — assert per-method parameter
  names and types via `typing.get_type_hints`.
- [x] 12. Add `MockVPNClient` conformance fixture in the test root for reuse
  by interop implementations.
- [x] 13. Add `test_vpnstatus_optional_self_address_for_twingate_pattern` —
  construct a `VPNStatus(self_address=None, provider="twingate", ...)` and
  assert no validation error.
