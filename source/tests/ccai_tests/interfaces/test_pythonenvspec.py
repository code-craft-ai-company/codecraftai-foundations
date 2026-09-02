"""
    .. module:: test_pythonenvspec
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Tests for PythonEnvironmentSpec validation and derived properties.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2026, Code Craft AI LLC"
__credits__ = []


import unittest

from ccai.interfaces.pythonenvspec import PythonEnvironmentSpec
from ccai.interfaces.schemavalidationerror import SchemaValidationError


class PythonEnvironmentSpecDefaultsTests(unittest.TestCase):

    def test_minimal_spec_carries_documented_defaults(self) -> None:
        spec = PythonEnvironmentSpec(path="/opt/venvs/app")
        self.assertEqual(spec.path, "/opt/venvs/app")
        self.assertIsNone(spec.name)
        self.assertEqual(spec.packages, [])
        self.assertEqual(spec.requirements_files, [])
        self.assertEqual(spec.constraints_files, [])
        self.assertEqual(spec.interpreter, "python3")
        self.assertFalse(spec.system_site_packages)
        self.assertTrue(spec.upgrade_pip)
        self.assertFalse(spec.upgrade_packages)
        self.assertFalse(spec.recreate)
        self.assertIsNone(spec.owner)
        self.assertIsNone(spec.index_url)
        self.assertEqual(spec.extra_index_urls, [])
        self.assertEqual(spec.trusted_hosts, [])
        self.assertEqual(spec.pip_options, [])
        return

    def test_lists_are_copied_not_aliased(self) -> None:
        packages = ["rich"]
        spec = PythonEnvironmentSpec(path="/opt/venvs/app", packages=packages)
        packages.append("six")
        self.assertEqual(spec.packages, ["rich"])
        return


class PythonEnvironmentSpecSlugTests(unittest.TestCase):

    def test_slug_prefers_explicit_name(self) -> None:
        spec = PythonEnvironmentSpec(path="/opt/venvs/app", name="agent")
        self.assertEqual(spec.slug, "agent")
        return

    def test_slug_is_derived_from_path(self) -> None:
        spec = PythonEnvironmentSpec(path="/opt/venvs/app")
        self.assertEqual(spec.slug, "opt-venvs-app")
        return

    def test_slug_replaces_unsafe_characters(self) -> None:
        spec = PythonEnvironmentSpec(path="/srv/my app/v1")
        self.assertEqual(spec.slug, "srv-my-app-v1")
        return


class PythonEnvironmentSpecIndexTests(unittest.TestCase):

    def test_has_index_configuration_false_by_default(self) -> None:
        spec = PythonEnvironmentSpec(path="/opt/venvs/app")
        self.assertFalse(spec.has_index_configuration)
        return

    def test_has_index_configuration_true_for_trusted_host_only(self) -> None:
        spec = PythonEnvironmentSpec(path="/opt/venvs/app", trusted_hosts=["pypi.internal:8443"])
        self.assertTrue(spec.has_index_configuration)
        return

    def test_index_url_accepts_https_and_file(self) -> None:
        PythonEnvironmentSpec(path="/opt/v", index_url="https://pypi.internal/simple")
        PythonEnvironmentSpec(path="/opt/v", extra_index_urls=["file:///srv/wheels"])
        return


class PythonEnvironmentSpecValidationTests(unittest.TestCase):

    def test_relative_path_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            PythonEnvironmentSpec(path="venvs/app")
        return

    def test_root_path_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            PythonEnvironmentSpec(path="/")
        return

    def test_newline_in_path_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            PythonEnvironmentSpec(path="/opt/v\nrm -rf /")
        return

    def test_bad_name_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            PythonEnvironmentSpec(path="/opt/v", name="../etc")
        return

    def test_empty_package_entry_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            PythonEnvironmentSpec(path="/opt/v", packages=["rich", ""])
        return

    def test_newline_in_package_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            PythonEnvironmentSpec(path="/opt/v", packages=["rich\ncurl evil"])
        return

    def test_constraints_without_requirements_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            PythonEnvironmentSpec(path="/opt/v", constraints_files=["/c.txt"])
        return

    def test_owner_accepts_user_and_user_group(self) -> None:
        PythonEnvironmentSpec(path="/opt/v", owner="agent")
        PythonEnvironmentSpec(path="/opt/v", owner="agent:staff")
        return

    def test_owner_with_shell_metachars_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            PythonEnvironmentSpec(path="/opt/v", owner="agent; rm -rf /")
        return

    def test_index_url_with_whitespace_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            PythonEnvironmentSpec(path="/opt/v", index_url="https://pypi.internal/simple x")
        return

    def test_index_url_with_bad_scheme_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            PythonEnvironmentSpec(path="/opt/v", index_url="ftp://pypi.internal/simple")
        return

    def test_trusted_host_with_path_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            PythonEnvironmentSpec(path="/opt/v", trusted_hosts=["pypi.internal/simple"])
        return

    def test_empty_interpreter_rejected(self) -> None:
        with self.assertRaises(SchemaValidationError):
            PythonEnvironmentSpec(path="/opt/v", interpreter="")
        return


class PythonEnvironmentSpecSerialisationTests(unittest.TestCase):

    def test_to_dict_from_dict_roundtrip(self) -> None:
        spec = PythonEnvironmentSpec(
            path="/opt/venvs/app", name="app", packages=["rich>=13"],
            requirements_files=["/srv/r.txt"], constraints_files=["/srv/c.txt"],
            interpreter="/usr/bin/python3.12", system_site_packages=True,
            upgrade_pip=False, upgrade_packages=True, recreate=True,
            owner="app:app", index_url="https://pypi.internal/simple",
            extra_index_urls=["https://extra.internal/simple"],
            trusted_hosts=["pypi.internal"], pip_options=["--no-cache-dir"],
        )
        restored = PythonEnvironmentSpec.from_dict(spec.to_dict())
        self.assertEqual(restored, spec)
        return

    def test_from_dict_rejects_invalid_payload(self) -> None:
        with self.assertRaises(SchemaValidationError):
            PythonEnvironmentSpec.from_dict({"path": "relative"})
        return


if __name__ == "__main__":
    unittest.main()
