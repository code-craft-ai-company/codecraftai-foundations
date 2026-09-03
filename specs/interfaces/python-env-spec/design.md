# Design

## Overview

`PythonEnvironmentSpec` mirrors `VPNJoinSpec` structurally: a `SchemaObject`
whose constructor validates every field and whose only methods are derived
properties. It lives in `ccai.interfaces` so that both the provisioning layer
(which renders it into cloud-init before a host is reachable) and the sysman
layer (which converges it through an `ICommandRunner` afterwards) depend on the
same shape without depending on each other.

## Fields

| Field | Type | Default | Notes |
|---|---|---|---|
| `path` | `str` | required | Absolute POSIX environment root |
| `name` | `str \| None` | `None` | Artefact label; derived from path when absent |
| `packages` | `list[str]` | `[]` | PEP 508 specifiers |
| `requirements_files` | `list[str]` | `[]` | `-r` files on the target host |
| `constraints_files` | `list[str]` | `[]` | `-c` files; require requirements files |
| `interpreter` | `str` | `"python3"` | Command that creates the environment |
| `system_site_packages` | `bool` | `False` | `--system-site-packages` |
| `upgrade_pip` | `bool` | `True` | Upgrade pip after creation |
| `upgrade_packages` | `bool` | `False` | `--upgrade` on installs |
| `recreate` | `bool` | `False` | Remove an existing environment first |
| `owner` | `str \| None` | `None` | `user[:group]` handed the finished tree |
| `index_url` | `str \| None` | `None` | Credential-free `--index-url` |
| `index_credential` | `str \| None` | `None` | Credential-vault reference applied to `index_url` and same-host extras; requires `index_url` |
| `extra_index_urls` | `list[str]` | `[]` | Credential-free `--extra-index-url` |
| `trusted_hosts` | `list[str]` | `[]` | `--trusted-host` entries |
| `pip_options` | `list[str]` | `[]` | Extra install tokens |

The names match `ccai.sysman.common.pythonenvironmentmanagementbase.PythonEnvSpec`
where the concepts overlap (`path`, `packages`, `requirements_files`,
`constraints_files`, `system_site_packages`, `upgrade_pip`, `upgrade_packages`,
`recreate`). `interpreter` is a single command string here (it lands on a shell
line) where the sysman dataclass takes an argv list; `owner` and the index fields
exist only here because a first-boot script runs as root and has no manager
config to read them from.

## Why No Credentials

Every string lands in a shell script that cloud-init logs world-readably on
some venues. The spec therefore accepts no token field and rejects URL
userinfo in `index_url` / `extra_index_urls`. A private index is declared by
naming a vault entry in `index_credential`, following
`VPNJoinSpec.control_plane_credential`: the provisioning engine resolves the
name at validate time (`BasicCredential`, `PersonalApiTokenCredential`, or a
token credential) and the renderer embeds it inside the root-only `0400`
pip configuration at render time.

## Module Layout

```
source/packages/ccai/interfaces/pythonenvspec.py
source/tests/ccai_tests/interfaces/test_pythonenvspec.py
```

## See Also

- `codecraftai-provisioning/specs/python-env-bootstrap/` — the renderer that
  consumes this spec.
- `codecraftai-sysman-common/specs/contracts/python-environment-management/contract.md`
  — the post-boot convergence contract with the matching field names.
