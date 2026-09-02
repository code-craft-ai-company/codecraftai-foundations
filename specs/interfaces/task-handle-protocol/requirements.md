# Requirements

## Introduction

The `task-handle-protocol` feature introduces `ITaskHandle` into
`codecraftai-interfaces`. The protocol captures the §6.6 decision in
PLAN-VPN-AND-CLOUD-PROVISIONING.md: vSphere (and other venues with
async APIs) must surface long-running operations as a *synchronous*
`TaskHandle` polled under Aspects control — not as `asyncio` tasks.
That decision keeps the mental model consistent with every other
ccai client.

This spec defines the *protocol only*. The reusable concrete
implementation lives in `codecraftai-restclient-base/task-handle-base`;
vendor-specific implementations live in `codecraftai-interop-vsphere`
and any other venue interop package that surfaces async APIs.

**See Also:** [task-handle-base](../../../codecraftai-restclient-base/specs/task-handle-base/design.md).

---

## Requirements

### Requirement 1: Task Handle Protocol Surface

**User Story:** As an interop client implementer, I want a uniform
contract for returning an async-task handle so callers do not learn
a new shape per venue.

#### Acceptance Criteria

1. THE SYSTEM SHALL declare `ITaskHandle(Protocol)` with the
   following methods:
   - `wait(aspects) -> TaskResult`
   - `cancel(aspects) -> None`
   - `is_done() -> bool`
   - `task_id() -> str`
2. THE SYSTEM SHALL define `TaskResult` as a `@dataclass` with
   fields: `task_id: str`, `state: TaskState`, `progress: int`,
   `error: Optional[str]`, `payload: Optional[dict]`.
3. THE SYSTEM SHALL define `TaskState(IntEnum)` with members
   `PENDING = 1`, `RUNNING = 2`, `SUCCEEDED = 3`, `FAILED = 4`,
   `CANCELLED = 5`.

---

### Requirement 2: Synchronous Wait Semantics

**User Story:** As a caller, I want `wait` to be a blocking sync
call whose pacing I control through Aspects, not an `await`able.

#### Acceptance Criteria

1. THE SYSTEM SHALL document `wait(aspects)` as a synchronous
   blocking call.
2. THE SYSTEM SHALL require implementations to drive the poll loop
   using `aspects.completion_interval` and
   `aspects.completion_timeout`.
3. WHEN `wait` times out THE SYSTEM SHALL require implementations
   to raise `TimeoutError` (not return a `FAILED` `TaskResult`).
4. IF the underlying task transitions to `FAILED` or `CANCELLED`
   before timeout THEN THE SYSTEM SHALL return the corresponding
   `TaskResult` rather than raise.

---

### Requirement 3: Cancellation Semantics

**User Story:** As a destroy/cleanup coordinator, I want to cancel
in-flight tasks so I can tear down cleanly.

#### Acceptance Criteria

1. THE SYSTEM SHALL declare `cancel(aspects) -> None`.
2. WHEN the task is already in a terminal state THE SYSTEM SHALL
   require implementations to treat `cancel` as a no-op.
3. WHERE the underlying API does not support cancellation THE
   SYSTEM SHALL allow implementations to raise
   `NotImplementedError`.

---

### Requirement 4: No Behaviour-Modifying Decorators

**User Story:** As a maintainer, I want the protocol's behaviour
to be controlled exclusively through Aspects.

#### Acceptance Criteria

1. THE SYSTEM SHALL require `wait` and `cancel` to accept
   `aspects: Aspects` as a keyword-only parameter.
2. IF an implementation adds `@retry` or any behaviour-modifying
   decorator to `wait` or `cancel` THEN THE SYSTEM SHALL be
   considered non-conformant.

---

### Requirement 5: No Third-Party Imports

**User Story:** As a downstream consumer, I want the protocol
module to remain dependency-free.

#### Acceptance Criteria

1. THE SYSTEM SHALL import only `typing`, `dataclasses`, `enum`,
   and `ccai.aspects.aspects` in `itaskhandle.py`.
