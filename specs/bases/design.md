# Design Document — Bases

## Overview

`ccai.bases` is the home for base classes that satisfy the foundations admission rule. It
starts with `Freezable` and is expected to stay small.

## Design Decisions

1. **A namespace of its own** — a base class is neither an interface nor an aspects carrier.
   Giving base classes their own subpackage avoids repeating the placement problem that put
   `Aspects` under an ad-hoc namespace.
2. **Freezable moves with its history** — the module came from `codecraftai-xmodules` through a
   history-preserving import, and xmodules re-exports it from here so nothing breaks.
3. **Implementation via `object.__setattr__`** — the frozen flag is set through `object` so the
   guard in `__setattr__` cannot block its own initialisation.

## Components and Interfaces

```
source/packages/ccai/bases/__init__.py
source/packages/ccai/bases/freezable.py       Freezable
source/tests/ccai_tests/bases/test_freezable.py
```

```python
class Freezable:
    def __init__(self) -> None
    def freeze(self) -> None
    def __setattr__(self, name: str, value: object) -> None   # raises AttributeError once frozen
```

## Testing Strategy

Tests cover assignment before freeze, refusal after freeze with the attribute named in the
message, and retention of frozen values.
