# Design

## Overview

`ITaskHandle` captures the synchronous-wait-on-async-API pattern the
framework adopts uniformly (§6.6 decision). Every interop client that
backs an async API — vSphere's `Task` objects are the prime example —
returns an `ITaskHandle` from long-running operations
(`create`, `clone`, `power`, `delete`, `deploy`). Callers drive the
poll loop synchronously via Aspects.

The protocol is intentionally narrow: four methods and one typed
result. The concrete reusable implementation
(`TaskHandle` on `codecraftai-restclient-base`) covers the REST-polling
case used by vSphere, Proxmox, Nutanix, and others. Vendor packages
that already model their own task object (libvirt, hypervisor native
bindings) implement `ITaskHandle` directly.

**See Also:** [task-handle-base](../../../codecraftai-restclient-base/specs/task-handle-base/design.md),
[vpn-control-plane-protocol](../vpn-control-plane-protocol/design.md).

---

## Architecture

```
+--------------------+   returns    +---------------------+
| Long-running API   +------------->+ ITaskHandle         |
|  e.g. VmGroup.clone|              |   wait(aspects)     |
|       VmGroup.power|              |   cancel(aspects)   |
+--------------------+              |   is_done()         |
                                    |   task_id()         |
                                    +----------+----------+
                                               |
                       implements              |
            +----------------------------------+----------------+
            |                                                   |
+-----------v----------+                          +-------------v---------+
| TaskHandle           |                          | VSphereTaskHandle     |
| (restclient-base)    |                          | (interop-vsphere,     |
| REST poll loop       |                          |  composes TaskHandle) |
+----------------------+                          +-----------------------+
```

---

## Data Model

```python
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional, Protocol

from ccai.aspects.aspects import Aspects


class TaskState(IntEnum):
    """
        Lifecycle state of an asynchronous remote task.
    """
    PENDING = 1
    RUNNING = 2
    SUCCEEDED = 3
    FAILED = 4
    CANCELLED = 5


@dataclass
class TaskResult:
    """
        Final or in-progress snapshot of an async task's state.

        :param task_id: Provider-assigned task identifier.
        :param state: TaskState value at observation time.
        :param progress: Integer percent complete (0-100) when known.
        :param error: Error string if state == FAILED, else None.
        :param payload: Provider-specific result payload, when any.
    """
    task_id: str
    state: TaskState
    progress: int = 0
    error: Optional[str] = None
    payload: Optional[dict] = None


class ITaskHandle(Protocol):
    """
        Protocol for a sync-poll handle on a remote async task.
    """

    def wait(self, *, aspects: Aspects) -> TaskResult:
        ...

    def cancel(self, *, aspects: Aspects) -> None:
        ...

    def is_done(self) -> bool:
        ...

    def task_id(self) -> str:
        ...
```

---

## Module Layout

```
codecraftai-interfaces/source/packages/ccai/interfaces/
  itaskhandle.py    <-- ITaskHandle, TaskResult, TaskState
```

---

## Wait Semantics

`wait(aspects)` is a synchronous blocking call. Implementations MUST:

- Drive the polling loop using `aspects.completion_interval` and
  `aspects.completion_timeout` (typical defaults: 10s interval,
  600s timeout — see `aspectsrest.py`).
- Raise `TimeoutError` when `completion_timeout` elapses without
  reaching a terminal state.
- Return a `TaskResult` with `state ∈ {SUCCEEDED, FAILED, CANCELLED}`
  otherwise — terminal states are not exceptions.

This split keeps the "the task finished but failed" case
distinguishable from "I gave up waiting" — a usability requirement
called out in the project standards' exception-handling rules.

---

## See Also

- [task-handle-base](../../../codecraftai-restclient-base/specs/task-handle-base/design.md)
  — the reusable REST-poll implementation of this protocol.
- [vpn-control-plane-protocol](../vpn-control-plane-protocol/design.md)
  — provider implementations may surface `mint_authkey` /
  `apply_acl` as task handles when the underlying API is async.

---

## Testing Strategy

- **Import test.** `ITaskHandle`, `TaskResult`, `TaskState` import
  and are exported via `__all__`.
- **Protocol-shape test.** Each method's signature matches the
  design.
- **Conformance fixture.** `MockTaskHandle` lives in the test root
  and drives a programmable state sequence
  (`[PENDING, RUNNING, RUNNING, SUCCEEDED]`) so concrete
  implementations can reuse the wait-loop tests.
- **No property tests required at the protocol layer** — the
  protocol itself carries no computation. The poll-loop math is
  property-tested in `task-handle-base`.
