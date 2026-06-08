"""
    Unit tests for the :mod:`ccai.interfaces.addressplane` module.

    Includes both example-based tests and hypothesis property tests covering
    the totality, idempotence, ordering, and round-trip invariants required
    by the :class:`IDeviceAddressSet` contract.
"""

import typing
import unittest
from typing import List, Optional, Tuple

from hypothesis import given
from hypothesis import strategies as st

from ccai.interfaces.addressplane import (
    AddressPlane,
    DeviceAddressSetSnapshot,
    IDeviceAddressSet,
)


optional_address_strategy = st.one_of(st.none(), st.text(min_size=1, max_size=64))
address_triple_strategy = st.tuples(
    optional_address_strategy,
    optional_address_strategy,
    optional_address_strategy,
)
plane_strategy = st.sampled_from(list(AddressPlane))


def _snapshot_from_triple(triple: Tuple[Optional[str], Optional[str], Optional[str]]) -> DeviceAddressSetSnapshot:
    pub, prv, ovl = triple
    snapshot = DeviceAddressSetSnapshot(
        public_address=pub,
        private_address=prv,
        overlay_address=ovl,
    )
    return snapshot


class TestAddressPlaneEnum(unittest.TestCase):
    """
        Verify the :class:`AddressPlane` enum.
    """

    def test_addressplane_members_present_and_ordered(self) -> None:
        """
            Exactly three members exist in ascending ordinal order.
        """
        members = list(AddressPlane)
        self.assertEqual(len(members), 3)
        self.assertEqual(members[0], AddressPlane.PUBLIC)
        self.assertEqual(members[1], AddressPlane.PRIVATE)
        self.assertEqual(members[2], AddressPlane.OVERLAY)
        self.assertEqual(int(AddressPlane.PUBLIC), 1)
        self.assertEqual(int(AddressPlane.PRIVATE), 2)
        self.assertEqual(int(AddressPlane.OVERLAY), 3)
        return

    def test_addressplane_no_magic_dns_member(self) -> None:
        """
            Magic DNS is not represented as a plane.
        """
        names = {m.name for m in AddressPlane}
        self.assertNotIn("MAGIC_DNS", names)
        return


class TestIDeviceAddressSetProtocol(unittest.TestCase):
    """
        Verify the :class:`IDeviceAddressSet` protocol shape.
    """

    def test_ideviceaddressset_is_protocol(self) -> None:
        """
            ``IDeviceAddressSet`` is a :class:`typing.Protocol`.
        """
        is_protocol = issubclass(IDeviceAddressSet, typing.Protocol)
        self.assertTrue(is_protocol)
        return

    def test_snapshot_satisfies_protocol(self) -> None:
        """
            The snapshot helper satisfies the protocol via runtime check.
        """
        snapshot = DeviceAddressSetSnapshot(public_address="1.2.3.4")
        is_instance = isinstance(snapshot, IDeviceAddressSet)
        self.assertTrue(is_instance)
        return


class TestDeviceAddressSetSnapshotExamples(unittest.TestCase):
    """
        Example-based tests for the snapshot helper.
    """

    def test_snapshot_address_for_returns_populated_or_none(self) -> None:
        """
            ``address_for`` returns the populated value or ``None``.
        """
        snapshot = DeviceAddressSetSnapshot(
            public_address="1.2.3.4",
            private_address=None,
            overlay_address="100.64.0.1",
        )
        self.assertEqual(snapshot.address_for(plane=AddressPlane.PUBLIC), "1.2.3.4")
        self.assertIsNone(snapshot.address_for(plane=AddressPlane.PRIVATE))
        self.assertEqual(snapshot.address_for(plane=AddressPlane.OVERLAY), "100.64.0.1")
        return

    def test_snapshot_planes_returns_ascending_populated_planes(self) -> None:
        """
            ``planes`` returns only populated planes, in ascending order.
        """
        snapshot = DeviceAddressSetSnapshot(
            public_address="1.2.3.4",
            private_address=None,
            overlay_address="100.64.0.1",
        )
        populated = snapshot.planes()
        self.assertEqual(populated, [AddressPlane.PUBLIC, AddressPlane.OVERLAY])
        return

    def test_snapshot_convenience_accessors_match_address_for(self) -> None:
        """
            The convenience accessors and ``address_for`` agree.
        """
        snapshot = DeviceAddressSetSnapshot(
            public_address="1.2.3.4",
            private_address="10.0.0.1",
            overlay_address="100.64.0.1",
        )
        self.assertEqual(snapshot.public(), snapshot.address_for(plane=AddressPlane.PUBLIC))
        self.assertEqual(snapshot.private(), snapshot.address_for(plane=AddressPlane.PRIVATE))
        self.assertEqual(snapshot.overlay(), snapshot.address_for(plane=AddressPlane.OVERLAY))
        return

    def test_snapshot_all_none_yields_empty_planes(self) -> None:
        """
            A snapshot with no populated planes returns an empty ``planes()``.
        """
        snapshot = DeviceAddressSetSnapshot()
        populated = snapshot.planes()
        self.assertEqual(populated, [])
        return


class TestDeviceAddressSetSnapshotProperties(unittest.TestCase):
    """
        Hypothesis property tests for the snapshot helper.

        Covers the totality, consistency, idempotence, ordering, accessor
        equivalence, and round-trip invariants demanded by the spec.
    """

    @given(triple=address_triple_strategy, plane=plane_strategy)
    def test_property_p1_totality(
        self,
        triple: Tuple[Optional[str], Optional[str], Optional[str]],
        plane: AddressPlane,
    ) -> None:
        """
            P1 — Totality: ``address_for`` returns ``str`` or ``None`` for
            every plane and every triple, never raises.
        """
        snapshot = _snapshot_from_triple(triple)
        result = snapshot.address_for(plane=plane)
        if result is not None:
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)
        return

    @given(triple=address_triple_strategy, plane=plane_strategy)
    def test_property_p2_has_consistent_with_address_for(
        self,
        triple: Tuple[Optional[str], Optional[str], Optional[str]],
        plane: AddressPlane,
    ) -> None:
        """
            P2 — ``has(plane) == (address_for(plane) is not None)``.
        """
        snapshot = _snapshot_from_triple(triple)
        addr = snapshot.address_for(plane=plane)
        expected = addr is not None
        self.assertEqual(snapshot.has(plane=plane), expected)
        return

    @given(triple=address_triple_strategy, plane=plane_strategy)
    def test_property_p3_idempotence(
        self,
        triple: Tuple[Optional[str], Optional[str], Optional[str]],
        plane: AddressPlane,
    ) -> None:
        """
            P3 — Idempotence: repeated ``address_for`` returns the same value.
        """
        snapshot = _snapshot_from_triple(triple)
        first = snapshot.address_for(plane=plane)
        second = snapshot.address_for(plane=plane)
        third = snapshot.address_for(plane=plane)
        self.assertEqual(first, second)
        self.assertEqual(second, third)
        return

    @given(triple=address_triple_strategy)
    def test_property_p4_planes_ascending(
        self,
        triple: Tuple[Optional[str], Optional[str], Optional[str]],
    ) -> None:
        """
            P4 — ``planes()`` returns populated planes in strictly ascending
            ordinal order.
        """
        snapshot = _snapshot_from_triple(triple)
        populated = snapshot.planes()
        as_ints: List[int] = [int(p) for p in populated]
        sorted_ints = sorted(as_ints)
        self.assertEqual(as_ints, sorted_ints)
        self.assertEqual(len(set(as_ints)), len(as_ints))
        for plane in populated:
            self.assertTrue(snapshot.has(plane=plane))
        return

    @given(triple=address_triple_strategy)
    def test_property_p5_convenience_equivalence(
        self,
        triple: Tuple[Optional[str], Optional[str], Optional[str]],
    ) -> None:
        """
            P5 — Convenience accessors equal ``address_for``.
        """
        snapshot = _snapshot_from_triple(triple)
        self.assertEqual(snapshot.public(), snapshot.address_for(plane=AddressPlane.PUBLIC))
        self.assertEqual(snapshot.private(), snapshot.address_for(plane=AddressPlane.PRIVATE))
        self.assertEqual(snapshot.overlay(), snapshot.address_for(plane=AddressPlane.OVERLAY))
        return

    @given(triple=address_triple_strategy)
    def test_property_p6_round_trip(
        self,
        triple: Tuple[Optional[str], Optional[str], Optional[str]],
    ) -> None:
        """
            P6 — Round-trip: constructing then querying yields the inputs.
        """
        pub, prv, ovl = triple
        snapshot = DeviceAddressSetSnapshot(
            public_address=pub,
            private_address=prv,
            overlay_address=ovl,
        )
        self.assertEqual(snapshot.address_for(plane=AddressPlane.PUBLIC), pub)
        self.assertEqual(snapshot.address_for(plane=AddressPlane.PRIVATE), prv)
        self.assertEqual(snapshot.address_for(plane=AddressPlane.OVERLAY), ovl)
        return


if __name__ == "__main__":
    unittest.main()
