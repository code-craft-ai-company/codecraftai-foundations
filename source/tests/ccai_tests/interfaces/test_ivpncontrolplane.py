"""
    Unit tests for the :mod:`ccai.interfaces.ivpncontrolplane` module.
"""

import dataclasses
import inspect
import typing
import unittest
from typing import List, Optional

from ccai.aspects.aspects import Aspects
from ccai.interfaces.ivpncontrolplane import IVPNControlPlane, VPNDeviceRecord


class MockVPNControlPlane:
    """
        Programmable :class:`IVPNControlPlane` conformance fixture.
    """

    def __init__(self) -> None:
        self._devices: List[VPNDeviceRecord] = []
        self._minted: List[str] = []
        self._applied_acls: List[dict] = []
        return

    def mint_authkey(
        self,
        *,
        reusable: bool,
        ephemeral: bool,
        tags: List[str],
        ttl_seconds: int,
        aspects: Aspects,
    ) -> str:
        rtnval = "tskey-mock-{}".format(len(self._minted))
        self._minted.append(rtnval)
        return rtnval

    def list_devices(self, *, aspects: Aspects) -> List[VPNDeviceRecord]:
        rtnval = list(self._devices)
        return rtnval

    def delete_device(self, *, device_id: str, aspects: Aspects) -> None:
        remaining: List[VPNDeviceRecord] = []
        for dev in self._devices:
            if dev.device_id != device_id:
                remaining.append(dev)
        self._devices = remaining
        return

    def apply_acl(self, *, acl_doc: dict, aspects: Aspects) -> None:
        self._applied_acls.append(acl_doc)
        return


class TestVPNDeviceRecordDataclass(unittest.TestCase):
    """
        Verify the shape of the :class:`VPNDeviceRecord` dataclass.
    """

    def test_vpndevicerecord_is_dataclass(self) -> None:
        """
            Confirm :class:`VPNDeviceRecord` is a dataclass.
        """
        is_dc = dataclasses.is_dataclass(VPNDeviceRecord)
        self.assertTrue(is_dc)
        return

    def test_vpndevicerecord_field_names(self) -> None:
        """
            Confirm the dataclass declares the expected fields.
        """
        fields = dataclasses.fields(VPNDeviceRecord)
        names = [f.name for f in fields]
        expected = [
            "device_id",
            "hostname",
            "overlay_address",
            "tags",
            "os",
            "last_seen",
        ]
        self.assertEqual(names, expected)
        return

    def test_vpndevicerecord_overlay_optional_for_twingate_pattern(self) -> None:
        """
            A record with ``overlay_address=None`` constructs without error.
        """
        record = VPNDeviceRecord(
            device_id="dev-1",
            hostname="connector-a",
            overlay_address=None,
            tags=["tag:lab"],
            os="linux",
            last_seen=None,
        )
        self.assertIsNone(record.overlay_address)
        self.assertEqual(record.device_id, "dev-1")
        return


class TestIVPNControlPlaneProtocol(unittest.TestCase):
    """
        Verify the contract shape of the :class:`IVPNControlPlane` protocol.
    """

    def test_ivpncontrolplane_importable(self) -> None:
        """
            The protocol class and its result dataclass are importable.
        """
        self.assertIsNotNone(IVPNControlPlane)
        self.assertIsNotNone(VPNDeviceRecord)
        return

    def test_ivpncontrolplane_is_protocol(self) -> None:
        """
            ``IVPNControlPlane`` is a :class:`typing.Protocol`.
        """
        is_protocol = issubclass(IVPNControlPlane, typing.Protocol)
        self.assertTrue(is_protocol)
        return

    def test_mint_authkey_signature(self) -> None:
        """
            ``mint_authkey`` has the documented parameters, all keyword-only,
            and returns ``str``.
        """
        sig = inspect.signature(IVPNControlPlane.mint_authkey)
        param_names = list(sig.parameters.keys())
        expected = ["self", "reusable", "ephemeral", "tags", "ttl_seconds", "aspects"]
        self.assertEqual(param_names, expected)
        params = sig.parameters
        for name in ("reusable", "ephemeral", "tags", "ttl_seconds", "aspects"):
            self.assertEqual(params[name].kind, inspect.Parameter.KEYWORD_ONLY)
        self.assertEqual(params["reusable"].annotation, bool)
        self.assertEqual(params["ephemeral"].annotation, bool)
        self.assertEqual(params["tags"].annotation, List[str])
        self.assertEqual(params["ttl_seconds"].annotation, int)
        self.assertEqual(params["aspects"].annotation, Aspects)
        self.assertEqual(sig.return_annotation, str)
        return

    def test_list_devices_signature(self) -> None:
        """
            ``list_devices`` declares ``aspects`` and returns a list of
            :class:`VPNDeviceRecord`.
        """
        sig = inspect.signature(IVPNControlPlane.list_devices)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "aspects"])
        self.assertEqual(params["aspects"].annotation, Aspects)
        self.assertEqual(params["aspects"].kind, inspect.Parameter.KEYWORD_ONLY)
        self.assertEqual(sig.return_annotation, List[VPNDeviceRecord])
        return

    def test_delete_device_signature(self) -> None:
        """
            ``delete_device`` declares ``device_id`` and ``aspects`` and
            returns ``None``.
        """
        sig = inspect.signature(IVPNControlPlane.delete_device)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "device_id", "aspects"])
        self.assertEqual(params["device_id"].annotation, str)
        self.assertEqual(params["device_id"].kind, inspect.Parameter.KEYWORD_ONLY)
        self.assertEqual(params["aspects"].annotation, Aspects)
        self.assertEqual(sig.return_annotation, None)
        return

    def test_apply_acl_signature(self) -> None:
        """
            ``apply_acl`` declares ``acl_doc`` and ``aspects`` and returns
            ``None``.
        """
        sig = inspect.signature(IVPNControlPlane.apply_acl)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "acl_doc", "aspects"])
        self.assertEqual(params["acl_doc"].annotation, dict)
        self.assertEqual(params["acl_doc"].kind, inspect.Parameter.KEYWORD_ONLY)
        self.assertEqual(params["aspects"].annotation, Aspects)
        self.assertEqual(sig.return_annotation, None)
        return

    def test_mock_implementation_satisfies_protocol(self) -> None:
        """
            The :class:`MockVPNControlPlane` fixture satisfies the protocol.
        """
        mock = MockVPNControlPlane()
        aspects = Aspects()
        key = mock.mint_authkey(
            reusable=False,
            ephemeral=True,
            tags=["tag:lab"],
            ttl_seconds=900,
            aspects=aspects,
        )
        self.assertTrue(key.startswith("tskey-mock-"))
        listed = mock.list_devices(aspects=aspects)
        self.assertEqual(listed, [])
        mock.apply_acl(acl_doc={"acls": []}, aspects=aspects)
        return


if __name__ == "__main__":
    unittest.main()
