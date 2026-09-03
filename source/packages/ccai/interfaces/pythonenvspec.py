"""
    .. module:: pythonenvspec
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Declarative Python virtual-environment specification attached to a CloudInstance.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


import os
import re

from typing import List, Optional

from ccai.interfaces.schemaobject import SchemaObject
from ccai.interfaces.schemafield import Field

from ccai.interfaces.schemavalidationerror import SchemaValidationError


_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,62}$")
_OWNER_PATTERN = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_-]{0,31}\$?(:[A-Za-z_][A-Za-z0-9_-]{0,31}\$?)?$"
)
_URL_PATTERN = re.compile(r"^(https?|file)://\S+$")
_URL_USERINFO_PATTERN = re.compile(r"^[A-Za-z]+://[^/@]+@")
_HOST_PATTERN = re.compile(r"^[A-Za-z0-9.-]+(:[0-9]{1,5})?$")

_DEFAULT_INTERPRETER = "python3"


def _require_non_empty_string(*, value: object, field_name: str) -> None:
    """
        Reject ``None``, non-``str``, empty, or newline-bearing values.

        Newlines are refused because every field ends up inside a shell
        script line; a newline would terminate the quoted token early.

        :param value: The candidate value.
        :param field_name: The field name for the error message.

        :raises: SchemaValidationError
    """
    if value is None or not isinstance(value, str) or len(value) == 0:
        raise SchemaValidationError(
            "{} must be a non-empty string.".format(field_name)
        )
    if "\n" in value or "\r" in value or "\x00" in value:
        raise SchemaValidationError(
            "{} must not contain newline or NUL characters.".format(field_name)
        )
    return


def _require_string_list(*, values: Optional[List[str]], field_name: str) -> List[str]:
    """
        Coerce an optional list of strings, validating each entry.

        :param values: The candidate list or ``None``.
        :param field_name: The field name for the error message.

        :returns: A new list (empty when ``values`` is ``None``).

        :raises: SchemaValidationError
    """
    if values is None:
        rtnval: List[str] = []
        return rtnval

    if not isinstance(values, (list, tuple)):
        raise SchemaValidationError("{} must be a list of strings.".format(field_name))

    rtnval = []
    for entry in values:
        _require_non_empty_string(value=entry, field_name="{} entry".format(field_name))
        rtnval.append(entry)
    return rtnval


class PythonEnvironmentSpec(SchemaObject):
    """
        Declarative Python virtual-environment specification.

        Carries everything a venue provisioner needs to inject a first-boot
        ``venv`` + ``pip`` bootstrap into the instance's cloud-init payload,
        and everything a post-boot ``python-environment-management`` sysman
        manager needs to converge the same environment later.  The field
        names mirror ``ccai.sysman.common.pythonenvironmentmanagementbase.
        PythonEnvSpec`` so a coordinator can translate between the two
        without a mapping table.

        No credential material is stored here.  ``index_url`` and
        ``extra_index_urls`` must be credential-free; a private index is
        declared by naming a credential-vault entry in
        ``index_credential`` (the way ``VPNJoinSpec.control_plane_credential``
        does), which the provisioning lifecycle resolves at validate time
        and injects at render time.
    """

    path = Field(str, required=True)
    name = Field(str, required=False, default=None)
    packages = Field(list, required=False, default=None)
    requirements_files = Field(list, required=False, default=None)
    constraints_files = Field(list, required=False, default=None)
    interpreter = Field(str, required=False, default=_DEFAULT_INTERPRETER)
    system_site_packages = Field(bool, required=False, default=False)
    upgrade_pip = Field(bool, required=False, default=True)
    upgrade_packages = Field(bool, required=False, default=False)
    recreate = Field(bool, required=False, default=False)
    owner = Field(str, required=False, default=None)
    index_url = Field(str, required=False, default=None)
    index_credential = Field(str, required=False, default=None)
    extra_index_urls = Field(list, required=False, default=None)
    trusted_hosts = Field(list, required=False, default=None)
    pip_options = Field(list, required=False, default=None)

    def __init__(self, *, path: str,
                 name: Optional[str] = None,
                 packages: Optional[List[str]] = None,
                 requirements_files: Optional[List[str]] = None,
                 constraints_files: Optional[List[str]] = None,
                 interpreter: str = _DEFAULT_INTERPRETER,
                 system_site_packages: bool = False,
                 upgrade_pip: bool = True,
                 upgrade_packages: bool = False,
                 recreate: bool = False,
                 owner: Optional[str] = None,
                 index_url: Optional[str] = None,
                 index_credential: Optional[str] = None,
                 extra_index_urls: Optional[List[str]] = None,
                 trusted_hosts: Optional[List[str]] = None,
                 pip_options: Optional[List[str]] = None) -> None:
        """
            Construct a PythonEnvironmentSpec.

            :param path: Absolute POSIX path of the environment root.
            :param name: Optional short label used to name the bootstrap
                         artefacts on the host; derived from ``path`` when
                         omitted.
            :param packages: PEP 508 requirement specifiers to install.
            :param requirements_files: ``-r`` files (paths on the target
                                       host).
            :param constraints_files: ``-c`` files applied to the
                                      requirements-file install.
            :param interpreter: Command used to create the environment
                                (``python3``, ``/usr/bin/python3.12``).
            :param system_site_packages: Create with
                                         ``--system-site-packages``.
            :param upgrade_pip: Upgrade pip inside the environment after
                                creation.
            :param upgrade_packages: Pass ``--upgrade`` on package installs.
            :param recreate: Remove an existing environment first.
            :param owner: Optional ``user`` or ``user:group`` the finished
                          tree is handed to (first-boot bootstrap runs as
                          root).
            :param index_url: Optional credential-free ``--index-url``.
            :param index_credential: Optional credential-vault reference
                                     (a ``BasicCredential`` or a token
                                     credential) applied to ``index_url``
                                     and to any ``extra_index_urls`` on
                                     the same host.  Requires
                                     ``index_url``.
            :param extra_index_urls: Optional credential-free
                                     ``--extra-index-url`` entries.
            :param trusted_hosts: Optional ``--trusted-host`` entries.
            :param pip_options: Extra tokens appended to every
                                ``pip install``.

            :raises: SchemaValidationError
        """
        _require_non_empty_string(value=path, field_name="path")
        if not path.startswith("/"):
            raise SchemaValidationError(
                "path must be an absolute POSIX path, got {!r}.".format(path)
            )
        if path == "/":
            raise SchemaValidationError("path must not be the filesystem root.")

        if name is not None:
            if not isinstance(name, str) or _NAME_PATTERN.match(name) is None:
                raise SchemaValidationError(
                    "name must match {} , got {!r}.".format(_NAME_PATTERN.pattern, name)
                )

        _require_non_empty_string(value=interpreter, field_name="interpreter")

        effective_packages = _require_string_list(values=packages, field_name="packages")
        effective_requirements = _require_string_list(
            values=requirements_files, field_name="requirements_files"
        )
        effective_constraints = _require_string_list(
            values=constraints_files, field_name="constraints_files"
        )
        effective_pip_options = _require_string_list(
            values=pip_options, field_name="pip_options"
        )

        if len(effective_constraints) > 0 and len(effective_requirements) == 0:
            raise SchemaValidationError(
                "constraints_files require at least one requirements_files entry."
            )

        if owner is not None:
            if not isinstance(owner, str) or _OWNER_PATTERN.match(owner) is None:
                raise SchemaValidationError(
                    "owner must be 'user' or 'user:group', got {!r}.".format(owner)
                )

        if index_url is not None:
            _require_non_empty_string(value=index_url, field_name="index_url")
            if _URL_PATTERN.match(index_url) is None:
                raise SchemaValidationError(
                    "index_url must be an http(s):// or file:// URL without "
                    "whitespace, got {!r}.".format(index_url)
                )
            if _URL_USERINFO_PATTERN.match(index_url) is not None:
                raise SchemaValidationError(
                    "index_url must not embed credentials; name a vault entry "
                    "in index_credential instead."
                )

        if index_credential is not None:
            _require_non_empty_string(value=index_credential,
                                      field_name="index_credential")
            if index_url is None:
                raise SchemaValidationError(
                    "index_credential requires index_url."
                )

        effective_extra_urls = _require_string_list(
            values=extra_index_urls, field_name="extra_index_urls"
        )
        for extra_url in effective_extra_urls:
            if _URL_PATTERN.match(extra_url) is None:
                raise SchemaValidationError(
                    "extra_index_urls entries must be http(s):// or file:// "
                    "URLs without whitespace, got {!r}.".format(extra_url)
                )
            if _URL_USERINFO_PATTERN.match(extra_url) is not None:
                raise SchemaValidationError(
                    "extra_index_urls entries must not embed credentials; name "
                    "a vault entry in index_credential instead."
                )

        effective_trusted_hosts = _require_string_list(
            values=trusted_hosts, field_name="trusted_hosts"
        )
        for host in effective_trusted_hosts:
            if _HOST_PATTERN.match(host) is None:
                raise SchemaValidationError(
                    "trusted_hosts entries must be host[:port], got {!r}.".format(host)
                )

        super().__init__(path=path, name=name,
                         packages=effective_packages,
                         requirements_files=effective_requirements,
                         constraints_files=effective_constraints,
                         interpreter=interpreter,
                         system_site_packages=bool(system_site_packages),
                         upgrade_pip=bool(upgrade_pip),
                         upgrade_packages=bool(upgrade_packages),
                         recreate=bool(recreate),
                         owner=owner,
                         index_url=index_url,
                         index_credential=index_credential,
                         extra_index_urls=effective_extra_urls,
                         trusted_hosts=effective_trusted_hosts,
                         pip_options=effective_pip_options)
        return

    @property
    def slug(self) -> str:
        """
            The label used to name per-environment artefacts on the host.

            ``name`` when supplied; otherwise the path with its leading
            slash removed and every character outside ``[A-Za-z0-9._-]``
            replaced by ``-`` (``/opt/venvs/app`` -> ``opt-venvs-app``).

            :returns: The slug.
        """
        if self.name is not None:
            rtnval = self.name
            return rtnval

        stripped = self.path.lstrip("/")
        rtnval = re.sub(r"[^A-Za-z0-9._-]+", "-", stripped).strip("-")
        if len(rtnval) == 0:
            rtnval = "env"
        return rtnval

    @property
    def has_index_configuration(self) -> bool:
        """
            Whether any of ``index_url`` / ``extra_index_urls`` /
            ``trusted_hosts`` is set.

            :returns: True when a pip configuration file is warranted.
        """
        if self.index_url is not None:
            rtnval = True
            return rtnval
        if self.extra_index_urls is not None and len(self.extra_index_urls) > 0:
            rtnval = True
            return rtnval
        if self.trusted_hosts is not None and len(self.trusted_hosts) > 0:
            rtnval = True
            return rtnval
        rtnval = False
        return rtnval


__all__ = ["PythonEnvironmentSpec"]
