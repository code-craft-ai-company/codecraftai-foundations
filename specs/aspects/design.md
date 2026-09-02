# Design Document — Aspects

## Overview

`ccai.aspects.aspects.Aspects` is the root of the suite's aspects hierarchy. Domain packages
subclass it with keyword-only constructors that forward the base fields and add their own.

## Design Decisions

1. **Unchanged on the move** — the class and its import path are exactly what interfaces
   shipped, so no consumer changes.
2. **Root of one hierarchy** — the richer interop `Aspects` becomes a subclass (consolidation
   phase 4), ending the situation where two unrelated classes shared the name.
3. **Stays a dataclass** — immutability for shared defaults is provided by subclasses that also
   derive from `ccai.bases.Freezable`, as the interop tier does.

## Components and Interfaces

```
source/packages/ccai/aspects/__init__.py
source/packages/ccai/aspects/aspects.py       Aspects
source/tests/ccai_tests/interfaces/test_aspects.py
```

## Testing Strategy

The existing tests cover defaults and overrides. Phase 4 adds a suite-level test in interop
asserting `issubclass(ccai.interop.aspects.Aspects, ccai.aspects.aspects.Aspects)`.
