# Implementation Plan: Aspects

## Overview

Carry the minimal `Aspects` into foundations unchanged, then unify the hierarchy.

## Tasks

- [x] 1. Move Aspects
  - [x] 1.1 Import `ccai/aspects` with history from `codecraftai-interfaces`
    - _Requirements: 1.1, 1.2_

- [ ] 2. Unify the hierarchy (phase 4 of the consolidation plan)
  - [ ] 2.1 Make `ccai.interop.aspects.Aspects` and `AspectsCmd` subclass this class
    - _Requirements: 2.1, 2.2_
  - [ ] 2.2 Subclass-relationship test in interop
    - _Requirements: 2.1_
