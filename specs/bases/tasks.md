# Implementation Plan: Bases

## Overview

Bring `Freezable` into foundations and leave a re-export behind in xmodules.

## Tasks

- [x] 1. Move Freezable
  - [x] 1.1 Import `freezable.py` with history as `ccai/bases/freezable.py`
    - _Requirements: 1.4_
  - [x] 1.2 Tests for freeze semantics
    - _Requirements: 1.1, 1.2, 1.3_

- [ ] 2. Re-export from xmodules (phase 4 of the consolidation plan)
  - [ ] 2.1 Replace `ccai/xmodules/freezable.py` with `from ccai.bases.freezable import Freezable`
    - _Requirements: 1.4_
