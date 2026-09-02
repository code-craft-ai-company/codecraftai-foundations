# Requirements Document — Bases

## Introduction

The Bases subpackage holds base classes that implementation packages across the suite derive
from and that meet the foundations admission rule. Today it contains `Freezable`, moved here from
`codecraftai-xmodules` because it is a pure base class with no dependencies whose only consumer
is the interop `Aspects` hierarchy.

## Glossary

- **Freezable**: A base class whose instances accept attribute assignment until `freeze()` is
  called and refuse it afterwards.

## Requirements

### Requirement 1: Freezable

**User Story:** As a package author, I want shared parameter objects to be immutable once
built, so that a module-level default cannot be modified by one caller and observed by another.

#### Acceptance Criteria

1. THE Freezable base SHALL allow attribute assignment before `freeze()` is called.
2. WHEN `freeze()` has been called, THE Freezable base SHALL raise `AttributeError` on any
   attribute assignment, and the message SHALL name the attribute.
3. THE Freezable base SHALL retain every attribute value set before freezing.
4. THE `freeze()` method SHALL return the instance so a frozen constant can be built in one
   expression.
5. THE Freezable base SHALL be importable as `ccai.bases.freezable.Freezable`, and
   `ccai.xmodules.freezable.Freezable` SHALL remain importable as a re-export until the suite
   has migrated.
