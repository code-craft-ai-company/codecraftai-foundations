# Implementation Plan — Task Handle Protocol

## Module and Models

- [x] 1. Create `automojo-interfaces/source/packages/automojo/interfaces/itaskhandle.py`.
- [x] 2. Define `TaskState(IntEnum)` with `PENDING=1`, `RUNNING=2`,
  `SUCCEEDED=3`, `FAILED=4`, `CANCELLED=5`.
- [x] 3. Define `TaskResult` dataclass with fields listed in the design.
- [x] 4. Define `ITaskHandle(Protocol)` with the four methods listed.
- [x] 5. Add module-level Sphinx docstring and per-method docstrings.

## ITaskHandle — To Implement

- [x] 6. Confirm `wait` and `cancel` declare `aspects: Aspects` as
  keyword-only.
- [x] 7. Confirm `is_done` and `task_id` take no parameters beyond
  `self`.
- [x] 8. Document the timeout-vs-terminal-state distinction in the
  `wait` docstring (raise `TimeoutError` on timeout, return
  `TaskResult` with terminal state otherwise).
- [x] 9. Add `__all__ = ["ITaskHandle", "TaskResult", "TaskState"]`.
- [x] 10. Confirm no third-party imports.

## Testing

- [x] 11. `test_itaskhandle_importable`.
- [x] 12. `test_taskstate_members_present`.
- [x] 13. `test_itaskhandle_is_protocol`.
- [x] 14. `test_itaskhandle_signature_shape` — assert parameter names
  and types via `typing.get_type_hints`.
- [x] 15. Add `MockTaskHandle` conformance fixture driving a
  programmable state sequence.
