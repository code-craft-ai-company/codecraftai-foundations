# Requirements Document — Aspects

## Introduction

The Aspects subpackage provides the minimal `Aspects` carrier that contract-layer protocols
accept and that every domain aspects class in the suite derives from. It moved here unchanged
from `codecraftai-interfaces`, where it lived under its own `ccai.aspects` namespace because
that repo was the only dependency-free place below the interop tier.

## Glossary

- **Aspects**: A dataclass carrying behaviour-modifying parameters: completion interval and
  timeout, connection timeout, maximum attempts and a logger name.
- **Domain aspects class**: A subclass such as `AspectsKubernetes` or the interop `Aspects`
  that adds fields for one domain.

## Requirements

### Requirement 1: Minimal Carrier

**User Story:** As a protocol author, I want to name an aspects type without depending on an
implementation package, so that contracts stay dependency-free.

#### Acceptance Criteria

1. THE Aspects class SHALL be a dataclass with `completion_interval`, `completion_timeout`,
   `connection_timeout`, `max_attempts` and `logger_name` fields with the documented defaults.
2. THE Aspects module SHALL import only from the standard library and `ccai.bases`.
3. THE Aspects class SHALL compare by identity and be hashable.
4. THE Aspects class SHALL derive from `Freezable` and SHALL NOT call `freeze()` in its own
   initialisation, so subclasses can add fields before freezing.

### Requirement 2: Single Hierarchy

**User Story:** As a caller, I want every aspects object in the suite to be an `Aspects`, so
that a function typed against the base accepts any domain aspects object.

#### Acceptance Criteria

1. EVERY domain aspects class in the suite SHALL derive from `ccai.aspects.aspects.Aspects`.
2. THE interop `ccai.interop.aspects.Aspects` and `AspectsCmd` SHALL derive from this class,
   adding their fields on top of the base five.
