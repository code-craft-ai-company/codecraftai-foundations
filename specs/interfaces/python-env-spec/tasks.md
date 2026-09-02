# Implementation Plan — python-env-spec

- [x] 1. Create `ccai.interfaces.pythonenvspec.PythonEnvironmentSpec`
- [x] 2. Constructor validation per requirements
- [x] 3. `slug` and `has_index_configuration` properties
- [x] 4. `test_pythonenvspec.py` (defaults, slug, index, validation, round-trip)
- [ ] 5. `index_credential` field naming a credential-vault entry (with the
  provisioning renderer minting it into the `0400` pip.conf)
- [ ] 6. Consider aliasing the sysman `PythonEnvSpec` dataclass to this schema
  object once the sysman maintenance coordinator exists
