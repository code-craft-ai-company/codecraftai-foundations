# Design Document — Aspects

## Overview

`ccai.aspects.aspects.Aspects` is the root of the suite's aspects hierarchy. Domain packages
subclass it with keyword-only constructors that forward the base fields and add their own.

## Design Decisions

1. **Unchanged on the move** — the class and its import path are exactly what interfaces
   shipped, so no consumer changes.
2. **Root of one hierarchy** — the richer interop `Aspects` becomes a subclass (consolidation
   phase 4), ending the situation where two unrelated classes shared the name.
3. **`eq=False` and `Freezable`** — a default dataclass compares by field and sets `__hash__`
   to `None`, which would make every subclass unhashable and change interop semantics. Aspects
   objects are behaviour carriers checked against shared defaults, so identity equality is the
   right semantics. The base inherits `Freezable` so every subclass shares one freeze mechanism,
   but it never freezes itself: freezing must follow the most-derived class's last assignment.
   Leaf classes call `freeze()` at the end of `__init__`; defaults are `Aspects().freeze()`.

## Components and Interfaces

```
source/packages/ccai/aspects/__init__.py
source/packages/ccai/aspects/aspects.py       Aspects
source/tests/ccai_tests/interfaces/test_aspects.py
```

## Testing Strategy

The existing tests cover defaults and overrides. Phase 4 adds a suite-level test in interop
asserting `issubclass(ccai.interop.aspects.Aspects, ccai.aspects.aspects.Aspects)`.
