# Requirements

## Introduction

The `python-env-spec` feature introduces `PythonEnvironmentSpec` into
`ccai.interfaces`. It is the declarative, venue-neutral description of a Python
virtual environment to deploy on a host — path, interpreter, packages,
requirements files, index configuration, ownership — shared by the
`codecraftai-provisioning` first-boot cloud-init renderer and, by field-name
parity, the `python-environment-management` sysman feature's own
`PythonEnvSpec`. It is a peer of `VPNJoinSpec`: a `SchemaObject` with strict
constructor validation, no behaviour, and no credential material.

---

## Requirements

### Requirement 1: Shape

1. THE SYSTEM SHALL expose `PythonEnvironmentSpec(SchemaObject)` from
   `ccai.interfaces.pythonenvspec` with the fields and defaults documented in
   `design.md`.
2. Optional list fields SHALL default to empty lists on the constructed object
   and SHALL be copied, never aliased, from the caller's list.

### Requirement 2: Validation

1. `path` SHALL be a non-empty absolute POSIX path other than `/`.
2. No string field SHALL contain a newline, carriage return, or NUL.
3. `name`, when given, SHALL match `[A-Za-z0-9][A-Za-z0-9._-]{0,62}`.
4. `owner`, when given, SHALL match `user` or `user:group`.
5. `index_url` and each `extra_index_urls` entry SHALL be an `http://`,
   `https://`, or `file://` URL with no whitespace.
6. Each `trusted_hosts` entry SHALL match `host[:port]`.
7. `constraints_files` SHALL require at least one `requirements_files` entry.
8. Every violation SHALL raise `SchemaValidationError`.

### Requirement 3: Derived Properties

1. `slug` SHALL return `name` when set, else the path with the leading slash
   removed and characters outside `[A-Za-z0-9._-]` collapsed to `-`.
2. `has_index_configuration` SHALL be True when any of `index_url`,
   `extra_index_urls`, `trusted_hosts` is set.

### Requirement 4: Serialisation

1. `to_dict` / `from_dict` SHALL round-trip to an equal object; `from_dict`
   SHALL re-run validation.
