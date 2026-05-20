"""
    Unit tests for the :mod:`automojo.interfaces.ivpnclient` module.
"""

import dataclasses
import inspect
import typing
import unittest
from typing import Dict, List, Optional

from automojo.aspects.aspects import Aspects
from automojo.interfaces.ivpnclient import IVPNClient, VPNStatus


class MockVPNClient:
    """
        Programmable :class:`IVPNClient` conformance fixture for reuse by
        interop-layer implementations in their own conformance tests.
    """

    def __init__(self) -> None:
        self._self_address: Optional[str] = None
        self._peers: Dict[str, str] = {}
        self._status: VPNStatus = VPNStatus(
            connected=False,
            backend_state="Stopped",
            self_address=None,
            hostname=None,
            tags=[],
            provider="mock",
        )
        return

    def bring_up(
        self,
        *,
        authkey: str,
        hostname: Optional[str],
        advertise_tags: Optional[List[str]],
        aspects: Aspects,
    ) -> VPNStatus:
        tags = advertise_tags if advertise_tags is not None else []
        self._status = VPNStatus(
            connected=True,
            backend_state="Running",
            self_address="100.64.0.1",
            hostname=hostname,
            tags=tags,
            provider="mock",
        )
        self._self_address = "100.64.0.1"
        return self._status

    def bring_down(self, *, aspects: Aspects) -> None:
        self._status = VPNStatus(
            connected=False,
            backend_state="Stopped",
            self_address=None,
            hostname=None,
            tags=[],
            provider="mock",
        )
        self._self_address = None
        return

    def status(self, *, aspects: Aspects) -> VPNStatus:
        rtnval = self._status
        return rtnval

    def self_address(self) -> Optional[str]:
        rtnval = self._self_address
        return rtnval

    def peer_addresses(self) -> Dict[str, str]:
        rtnval = dict(self._peers)
        return rtnval


class TestVPNStatusDataclass(unittest.TestCase):
    """
        Verify the shape and defaults of the :class:`VPNStatus` dataclass.
    """

    def test_vpnstatus_is_dataclass(self) -> None:
        """
            Confirm :class:`VPNStatus` is a dataclass.
        """
        is_dc = dataclasses.is_dataclass(VPNStatus)
        self.assertTrue(is_dc)
        return

    def test_vpnstatus_field_names(self) -> None:
        """
            Confirm the dataclass declares the expected field names.
        """
        fields = dataclasses.fields(VPNStatus)
        names = [f.name for f in fields]
        expected = [
            "connected",
            "backend_state",
            "self_address",
            "hostname",
            "tags",
            "provider",
        ]
        self.assertEqual(names, expected)
        return

    def test_vpnstatus_optional_self_address_for_twingate_pattern(self) -> None:
        """
            Verify a Twingate-pattern status (no overlay IP) constructs without
            raising.
        """
        status = VPNStatus(
            connected=True,
            backend_state="Running",
            self_address=None,
            hostname="connector-1",
            tags=[],
            provider="twingate",
        )
        self.assertIsNone(status.self_address)
        self.assertEqual(status.provider, "twingate")
        return


class TestIVPNClientProtocol(unittest.TestCase):
    """
        Verify the contract shape of the :class:`IVPNClient` protocol.
    """

    def test_ivpnclient_importable(self) -> None:
        """
            The protocol class and its result dataclass are importable.
        """
        self.assertIsNotNone(IVPNClient)
        self.assertIsNotNone(VPNStatus)
        return

    def test_ivpnclient_is_protocol(self) -> None:
        """
            ``IVPNClient`` is a :class:`typing.Protocol`.
        """
        is_protocol = issubclass(IVPNClient, typing.Protocol)
        self.assertTrue(is_protocol)
        return

    def test_ivpnclient_bring_up_signature(self) -> None:
        """
            ``bring_up`` declares the documented parameter names, types, and
            return annotation.
        """
        sig = inspect.signature(IVPNClient.bring_up)
        param_names = list(sig.parameters.keys())
        expected_names = ["self", "authkey", "hostname", "advertise_tags", "aspects"]
        self.assertEqual(param_names, expected_names)
        params = sig.parameters
        self.assertEqual(params["authkey"].annotation, str)
        self.assertEqual(params["hostname"].annotation, Optional[str])
        self.assertEqual(params["advertise_tags"].annotation, Optional[List[str]])
        self.assertEqual(params["aspects"].annotation, Aspects)
        self.assertEqual(sig.return_annotation, VPNStatus)
        return

    def test_ivpnclient_bring_up_keyword_only(self) -> None:
        """
            ``bring_up`` parameters after ``self`` are keyword-only.
        """
        sig = inspect.signature(IVPNClient.bring_up)
        params = sig.parameters
        for name in ("authkey", "hostname", "advertise_tags", "aspects"):
            kind = params[name].kind
            self.assertEqual(kind, inspect.Parameter.KEYWORD_ONLY)
        return

    def test_ivpnclient_bring_down_signature(self) -> None:
        """
            ``bring_down`` declares ``aspects`` and returns ``None``.
        """
        sig = inspect.signature(IVPNClient.bring_down)
        param_names = list(sig.parameters.keys())
        self.assertEqual(param_names, ["self", "aspects"])
        params = sig.parameters
        self.assertEqual(params["aspects"].annotation, Aspects)
        self.assertEqual(params["aspects"].kind, inspect.Parameter.KEYWORD_ONLY)
        self.assertEqual(sig.return_annotation, None)
        return

    def test_ivpnclient_status_signature(self) -> None:
        """
            ``status`` declares ``aspects`` and returns :class:`VPNStatus`.
        """
        sig = inspect.signature(IVPNClient.status)
        params = sig.parameters
        self.assertEqual(list(params.keys()), ["self", "aspects"])
        self.assertEqual(params["aspects"].annotation, Aspects)
        self.assertEqual(params["aspects"].kind, inspect.Parameter.KEYWORD_ONLY)
        self.assertEqual(sig.return_annotation, VPNStatus)
        return

    def test_ivpnclient_self_address_signature(self) -> None:
        """
            ``self_address`` has no parameters beyond ``self`` and returns
            ``Optional[str]``.
        """
        sig = inspect.signature(IVPNClient.self_address)
        param_names = list(sig.parameters.keys())
        self.assertEqual(param_names, ["self"])
        self.assertEqual(sig.return_annotation, Optional[str])
        return

    def test_ivpnclient_peer_addresses_signature(self) -> None:
        """
            ``peer_addresses`` has no parameters beyond ``self`` and returns a
            mapping.
        """
        sig = inspect.signature(IVPNClient.peer_addresses)
        param_names = list(sig.parameters.keys())
        self.assertEqual(param_names, ["self"])
        self.assertEqual(sig.return_annotation, Dict[str, str])
        return

    def test_mock_implementation_satisfies_protocol(self) -> None:
        """
            The :class:`MockVPNClient` fixture satisfies the protocol.
        """
        mock = MockVPNClient()
        aspects = Aspects()
        status = mock.bring_up(
            authkey="tskey-mock",
            hostname="host-1",
            advertise_tags=["tag:lab"],
            aspects=aspects,
        )
        self.assertTrue(status.connected)
        self.assertEqual(mock.self_address(), "100.64.0.1")
        self.assertEqual(mock.peer_addresses(), {})
        mock.bring_down(aspects=aspects)
        self.assertIsNone(mock.self_address())
        return


if __name__ == "__main__":
    unittest.main()
