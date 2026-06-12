"""
    Unit tests for :mod:`ccai.waiting.waitmodel` covering ``WaitGate``,
    ``WaitingScope``, and the ``TimeoutContext`` accessors/mutators.

    These exercise the surfaces that previously had no coverage (which is how the
    blank-timeout-message and broken-context-manager bugs went undetected). All
    timeouts are tiny so the suite stays fast.
"""

import threading
import unittest

from ccai.waiting.constants import TimeoutState
from ccai.waiting.waitmodel import TimeoutContext, WaitGate, WaitingScope


class TestWaitGate(unittest.TestCase):
    """
        Verify :class:`WaitGate` set/clear/wait semantics and timeout messaging.
    """

    def test_set_clear_is_set(self) -> None:
        gate = WaitGate(threading.Event())
        self.assertFalse(gate.is_set())
        gate.set()
        self.assertTrue(gate.is_set())
        gate.clear()
        self.assertFalse(gate.is_set())
        return

    def test_wait_returns_true_when_already_set(self) -> None:
        event = threading.Event()
        event.set()
        gate = WaitGate(event, timeout=0.01)
        self.assertTrue(gate.wait())
        return

    def test_wait_returns_false_on_timeout_without_raise(self) -> None:
        gate = WaitGate(threading.Event(), timeout=0.01)
        self.assertFalse(gate.wait())
        return

    def test_wait_raises_descriptive_timeout_message(self) -> None:
        # Regression: previously raised TimeoutError("") ignoring message/args.
        gate = WaitGate(
            threading.Event(),
            message="gate never opened",
            timeout=0.01,
            timeout_args=["host=alpha", "op=connect"]
        )
        with self.assertRaises(TimeoutError) as ctx:
            gate.wait(raise_timeout=True)
        text = str(ctx.exception)
        self.assertIn("gate never opened", text)
        self.assertIn("TIMEOUT:", text)
        self.assertIn("host=alpha", text)
        return

    def test_wait_default_message_when_none_supplied(self) -> None:
        gate = WaitGate(threading.Event(), timeout=0.01)
        with self.assertRaises(TimeoutError) as ctx:
            gate.wait(raise_timeout=True)
        self.assertGreater(len(str(ctx.exception)), 0)
        return


class TestWaitingScope(unittest.TestCase):
    """
        Verify :class:`WaitingScope` context-manager binding and gate coordination.
    """

    def test_enter_returns_scope_and_clears_gates(self) -> None:
        # Regression: __enter__ previously returned None, so the as-binding was unusable.
        e1 = threading.Event()
        e1.set()
        gate = WaitGate(e1, timeout=0.01)
        with WaitingScope([gate]) as scope:
            self.assertIsNotNone(scope)
            self.assertIsInstance(scope, WaitingScope)
            self.assertFalse(gate.is_set())  # cleared on entry
        return

    def test_wait_returns_when_all_gates_set(self) -> None:
        e1 = threading.Event()
        e2 = threading.Event()
        e1.set()
        e2.set()
        scope = WaitingScope([WaitGate(e1, timeout=0.01), WaitGate(e2, timeout=0.01)])
        # All gates already set; wait returns without blocking.
        scope.wait()
        return


class TestTimeoutContext(unittest.TestCase):
    """
        Verify :class:`TimeoutContext` accessors and mutators.
    """

    def test_has_timed_out_false_before_begin(self) -> None:
        # Regression: previously raised TypeError comparing None > None.
        tc = TimeoutContext(timeout=5)
        self.assertFalse(tc.has_timed_out)
        return

    def test_mark_begin_sets_running_state(self) -> None:
        tc = TimeoutContext(timeout=5)
        tc.mark_begin()
        self.assertEqual(tc._wait_state, TimeoutState.Running)
        self.assertIsNotNone(tc.end_time)
        return

    def test_extend_timeout_pushes_end_time_out(self) -> None:
        tc = TimeoutContext(timeout=5)
        tc.mark_begin()
        before = tc.end_time
        tc.extend_timeout(seconds=10)
        self.assertGreater(tc.end_time, before)
        return

    def test_reduce_delay(self) -> None:
        tc = TimeoutContext(timeout=5, delay=3)
        tc.reduce_delay(secs=1)
        self.assertEqual(tc.delay, 2)
        tc.reduce_delay(secs=5)
        self.assertEqual(tc.delay, 0)
        return

    def test_is_do_every_interval(self) -> None:
        tc = TimeoutContext(timeout=5, doevery=2)
        # loop_counter starts at 0 -> 0 % 2 == 0 -> True
        self.assertTrue(tc.is_do_every_interval)
        return


if __name__ == "__main__":
    unittest.main()
