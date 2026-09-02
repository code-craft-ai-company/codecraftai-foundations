"""
    .. module:: test_xtraceback
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Unit tests covering the helpers in :mod:`ccai.errors.xtraceback`.

    .. moduleauthor:: Code Craft AI
"""

import inspect
import os
import unittest

from typing import Dict, List
from unittest import mock

from ccai.errors import xtraceback


class TestTracebackFormatPolicy(unittest.TestCase):
    """
        Verifies the :class:`TracebackFormatPolicy` constants and the valid
        policy list.
    """

    def test_policy_constants(self) -> None:
        """
            Verifies the documented policy constants exist and have the right
            string values.

            :returns: ``None``
        """
        self.assertEqual(xtraceback.TracebackFormatPolicy.Brief, "Brief")
        self.assertEqual(xtraceback.TracebackFormatPolicy.Full, "Full")
        self.assertEqual(xtraceback.TracebackFormatPolicy.Hide, "Hide")
        return

    def test_valid_policy_list_contents(self) -> None:
        """
            Verifies the valid policy list includes all policy constants.

            :returns: ``None``
        """
        valid = xtraceback.VALID_MEMBER_TRACE_POLICY
        self.assertIn(xtraceback.TracebackFormatPolicy.Brief, valid)
        self.assertIn(xtraceback.TracebackFormatPolicy.Full, valid)
        self.assertIn(xtraceback.TracebackFormatPolicy.Hide, valid)
        self.assertEqual(len(valid), 3)
        return


class TestTracebackConfig(unittest.TestCase):
    """
        Verifies that the global :class:`TRACEBACK_CONFIG` defaults exist.
    """

    def test_traceback_config_defaults(self) -> None:
        """
            Verifies the documented defaults on :class:`TRACEBACK_CONFIG`.

            :returns: ``None``
        """
        self.assertIsNone(xtraceback.TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE)
        self.assertEqual(xtraceback.TRACEBACK_CONFIG.TRACEBACK_MAX_FULL_DISPLAY, 5)
        self.assertEqual(xtraceback.TRACEBACK_CONFIG.TRACEBACK_EXPAND_FIRST_N, 1)
        return


class TestSplitAndIndentLines(unittest.TestCase):
    """
        Verifies :func:`split_and_indent_lines` for indentation, prestripping,
        and edge cases.
    """

    def test_indent_single_level(self) -> None:
        """
            Verifies indenting a single line at level 1.

            :returns: ``None``
        """
        result = xtraceback.split_and_indent_lines(msg="hello", level=1)
        self.assertEqual(result, ["    hello"])
        return

    def test_indent_multiple_levels(self) -> None:
        """
            Verifies the indent multiplies with level.

            :returns: ``None``
        """
        result = xtraceback.split_and_indent_lines(msg="hi", level=3, indent=2)
        self.assertEqual(result, ["      hi"])
        return

    def test_split_multiline(self) -> None:
        """
            Verifies that multi-line input gets each line indented.

            :returns: ``None``
        """
        msg = "a\nb\nc"
        result = xtraceback.split_and_indent_lines(msg=msg, level=1, indent=2)
        self.assertEqual(result, ["  a", "  b", "  c"])
        return

    def test_pre_strip_leading_default(self) -> None:
        """
            Verifies the default pre-strip behaviour removes the smallest
            common leading indentation before re-indenting.

            :returns: ``None``
        """
        msg = "    a\n    b"
        result = xtraceback.split_and_indent_lines(msg=msg, level=1, indent=2)
        self.assertEqual(result, ["  a", "  b"])
        return

    def test_pre_strip_disabled(self) -> None:
        """
            Verifies that disabling pre-strip preserves original indentation.

            :returns: ``None``
        """
        msg = "    a\n    b"
        result = xtraceback.split_and_indent_lines(
            msg=msg,
            level=1,
            indent=2,
            pre_strip_leading=False
        )
        self.assertEqual(result, ["      a", "      b"])
        return

    def test_indent_level_zero(self) -> None:
        """
            Verifies that a level of 0 results in no indentation.

            :returns: ``None``
        """
        result = xtraceback.split_and_indent_lines(msg="hi", level=0)
        self.assertEqual(result, ["hi"])
        return

    def test_empty_message(self) -> None:
        """
            Verifies the helper handles an empty message.

            :returns: ``None``
        """
        result = xtraceback.split_and_indent_lines(msg="", level=2)
        self.assertEqual(result, [])
        return


class TestIsField(unittest.TestCase):
    """
        Verifies :func:`is_field` returns the right answer for a variety of
        inputs.
    """

    def test_int_is_field(self) -> None:
        """
            Verifies a plain int is considered a field.

            :returns: ``None``
        """
        result = xtraceback.is_field(42)
        self.assertTrue(result)
        return

    def test_string_is_field(self) -> None:
        """
            Verifies a plain string is considered a field.

            :returns: ``None``
        """
        result = xtraceback.is_field("hello")
        self.assertTrue(result)
        return

    def test_dict_is_field(self) -> None:
        """
            Verifies a dict is considered a field.

            :returns: ``None``
        """
        result = xtraceback.is_field({"a": 1})
        self.assertTrue(result)
        return

    def test_function_is_not_field(self) -> None:
        """
            Verifies a function is not considered a field.

            :returns: ``None``
        """
        def candidate() -> None:
            return
        result = xtraceback.is_field(candidate)
        self.assertFalse(result)
        return

    def test_class_is_not_field(self) -> None:
        """
            Verifies a class is not considered a field.

            :returns: ``None``
        """
        class Foo:
            pass
        result = xtraceback.is_field(Foo)
        self.assertFalse(result)
        return

    def test_module_is_not_field(self) -> None:
        """
            Verifies a module is not considered a field.

            :returns: ``None``
        """
        result = xtraceback.is_field(os)
        self.assertFalse(result)
        return

    def test_generator_function_is_not_field(self) -> None:
        """
            Verifies a generator function is not considered a field.

            :returns: ``None``
        """
        def gen():
            yield 1
        result = xtraceback.is_field(gen)
        self.assertFalse(result)
        return


class TestEnhancedErrorMixIn(unittest.TestCase):
    """
        Verifies :class:`EnhancedErrorMixIn` context capture.
    """

    def test_initial_contexts_empty(self) -> None:
        """
            Verifies the contexts dictionary starts empty.

            :returns: ``None``
        """
        mixin = xtraceback.EnhancedErrorMixIn()
        contexts = mixin.contexts
        is_dict = isinstance(contexts, dict)
        self.assertTrue(is_dict)
        self.assertEqual(len(contexts), 0)
        return

    def test_add_context_records_direct_caller(self) -> None:
        """
            Verifies that :meth:`EnhancedErrorMixIn.add_context` records the
            content under the *direct* caller's function name (not the
            caller-of-caller, which was the prior misattribution bug).

            :returns: ``None``
        """
        mixin = xtraceback.EnhancedErrorMixIn()

        def helper(target: xtraceback.EnhancedErrorMixIn) -> None:
            target.add_context(content="info goes here", label="HINT")
            return

        helper(target=mixin)

        contexts = mixin.contexts
        # The direct caller of add_context is ``helper``.
        is_present = "helper" in contexts
        self.assertTrue(is_present)
        recorded = contexts["helper"]
        self.assertEqual(recorded["label"], "HINT")
        self.assertEqual(recorded["content"], "info goes here")
        return

    def test_add_context_default_label(self) -> None:
        """
            Verifies that the default label is ``"CONTEXT"``.

            :returns: ``None``
        """
        mixin = xtraceback.EnhancedErrorMixIn()

        def helper(target: xtraceback.EnhancedErrorMixIn) -> None:
            target.add_context(content="data")
            return

        helper(target=mixin)

        contexts = mixin.contexts
        is_present = "helper" in contexts
        self.assertTrue(is_present)
        recorded = contexts["helper"]
        self.assertEqual(recorded["label"], "CONTEXT")
        return

    def test_add_context_at_module_scope_does_not_raise(self) -> None:
        """
            Verifies that recording context from a shallow stack does not raise
            ``IndexError`` (the prior bug raised at module scope).

            :returns: ``None``
        """
        mixin = xtraceback.EnhancedErrorMixIn()
        # Called directly from the test method (a valid, shallow-ish stack); the
        # clamp in _caller_scope_name guarantees no IndexError regardless of depth.
        mixin.add_context(content="data", label="L")
        contexts = mixin.contexts
        self.assertEqual(len(contexts), 1)
        return


class TestDataclasses(unittest.TestCase):
    """
        Verifies the dataclass containers used by the traceback helpers.
    """

    def test_origin_detail_construction(self) -> None:
        """
            Verifies :class:`OriginDetail` accepts and stores its fields.

            :returns: ``None``
        """
        origin = xtraceback.OriginDetail(file="a.py", lineno=12, scope="myfunc")
        self.assertEqual(origin.file, "a.py")
        self.assertEqual(origin.lineno, 12)
        self.assertEqual(origin.scope, "myfunc")
        return

    def test_trace_detail_construction(self) -> None:
        """
            Verifies :class:`TraceDetail` accepts and stores its fields.

            :returns: ``None``
        """
        origin = xtraceback.OriginDetail(file="a.py", lineno=1, scope="x")
        td = xtraceback.TraceDetail(
            origin=origin,
            call="x()",
            code=["1: pass"],
            context=None
        )
        self.assertEqual(td.origin, origin)
        self.assertEqual(td.call, "x()")
        self.assertEqual(td.code, ["1: pass"])
        self.assertIsNone(td.context)
        return

    def test_traceback_detail_construction(self) -> None:
        """
            Verifies :class:`TracebackDetail` accepts and stores its fields.

            :returns: ``None``
        """
        origin = xtraceback.OriginDetail(file="a.py", lineno=1, scope="x")
        td = xtraceback.TraceDetail(origin=origin, call="x()", code=[], context=None)
        tbd = xtraceback.TracebackDetail(
            extype="ValueError",
            exargs=["'oops'"],
            traces=[td]
        )
        self.assertEqual(tbd.extype, "ValueError")
        self.assertEqual(tbd.exargs, ["'oops'"])
        self.assertEqual(len(tbd.traces), 1)
        return


class TestFormatTracebackDetail(unittest.TestCase):
    """
        Verifies :func:`format_traceback_detail` produces a human-readable
        list of lines.
    """

    def _make_simple_detail(self) -> xtraceback.TracebackDetail:
        """
            Builds a minimal :class:`TracebackDetail` for formatting tests.

            :returns: A :class:`TracebackDetail` with one trace.
        """
        origin = xtraceback.OriginDetail(file="a.py", lineno=10, scope="myfunc")
        trace = xtraceback.TraceDetail(
            origin=origin,
            call="myfunc(x=1)",
            code=["010: def myfunc(x):"],
            context=None
        )
        rtnval = xtraceback.TracebackDetail(
            extype="ValueError",
            exargs=["'oops'"],
            traces=[trace]
        )
        return rtnval

    def test_format_includes_extype_and_args(self) -> None:
        """
            Verifies the formatted lines include the exception type and args.

            :returns: ``None``
        """
        detail = self._make_simple_detail()
        lines = xtraceback.format_traceback_detail(detail)
        is_list = isinstance(lines, list)
        self.assertTrue(is_list)
        joined = os.linesep.join(lines)
        self.assertIn("ValueError", joined)
        self.assertIn("'oops'", joined)
        return

    def test_format_includes_traceback_header(self) -> None:
        """
            Verifies the formatted output contains the documented header line.

            :returns: ``None``
        """
        detail = self._make_simple_detail()
        lines = xtraceback.format_traceback_detail(detail)
        joined = os.linesep.join(lines)
        self.assertIn("Traceback (most recent call first):", joined)
        return

    def test_format_includes_origin_metadata(self) -> None:
        """
            Verifies the formatted output contains file, line and scope.

            :returns: ``None``
        """
        detail = self._make_simple_detail()
        lines = xtraceback.format_traceback_detail(detail)
        joined = os.linesep.join(lines)
        self.assertIn("a.py", joined)
        self.assertIn("10", joined)
        self.assertIn("myfunc", joined)
        return

    def test_format_includes_call_when_present(self) -> None:
        """
            Verifies that a non-empty call is included in the formatted output.

            :returns: ``None``
        """
        detail = self._make_simple_detail()
        lines = xtraceback.format_traceback_detail(detail)
        joined = os.linesep.join(lines)
        self.assertIn("myfunc(x=1)", joined)
        return

    def test_format_includes_code_when_present(self) -> None:
        """
            Verifies that non-empty code lines are included in the output.

            :returns: ``None``
        """
        detail = self._make_simple_detail()
        lines = xtraceback.format_traceback_detail(detail)
        joined = os.linesep.join(lines)
        self.assertIn("def myfunc(x):", joined)
        return

    def test_format_with_empty_call_and_code(self) -> None:
        """
            Verifies that the formatter handles an empty call and empty code.

            :returns: ``None``
        """
        origin = xtraceback.OriginDetail(file="b.py", lineno=1, scope="other")
        trace = xtraceback.TraceDetail(origin=origin, call="", code=[], context=None)
        detail = xtraceback.TracebackDetail(
            extype="RuntimeError",
            exargs=[],
            traces=[trace]
        )
        lines = xtraceback.format_traceback_detail(detail)
        joined = os.linesep.join(lines)
        self.assertIn("RuntimeError", joined)
        self.assertIn("b.py", joined)
        return

    def test_format_no_traces(self) -> None:
        """
            Verifies the formatter handles a detail with no traces.

            :returns: ``None``
        """
        detail = xtraceback.TracebackDetail(
            extype="RuntimeError",
            exargs=[],
            traces=[]
        )
        lines = xtraceback.format_traceback_detail(detail)
        is_list = isinstance(lines, list)
        self.assertTrue(is_list)
        # The first two lines (header + "Traceback...") are always present.
        self.assertGreaterEqual(len(lines), 2)
        return


class TestCreateTracebackDetail(unittest.TestCase):
    """
        Verifies :func:`create_traceback_detail` shapes its output correctly.

        The function walks live frames; we use mocks to feed it a deterministic
        synthetic frame list so the test is not coupled to local filesystem
        state.
    """

    def test_create_returns_traceback_detail(self) -> None:
        """
            Verifies the function returns a :class:`TracebackDetail` whose
            extype matches the exception class name and whose traces list is
            populated when frames are available.

            :returns: ``None``
        """
        frame_detail = xtraceback.FrameDetail(
            name="myfunc",
            line_no=42,
            line_code="raise ValueError('oops')",
            filename="synthetic.py",
            co_module=None,
            co_code=None,
            args={"x": 1},
            first_line=40,
            last_line=45,
            code_lines=["040: pass"]
        )

        with mock.patch.object(
            xtraceback,
            "collect_stack_frames",
            return_value=[frame_detail]
        ):
            ex_inst = ValueError("oops")
            tb_detail = xtraceback.create_traceback_detail(ex_inst)

        self.assertEqual(tb_detail.extype, "ValueError")
        self.assertEqual(tb_detail.exargs, ["'oops'"])
        self.assertEqual(len(tb_detail.traces), 1)
        first_trace = tb_detail.traces[0]
        self.assertEqual(first_trace.origin.file, "synthetic.py")
        self.assertEqual(first_trace.origin.lineno, 42)
        self.assertEqual(first_trace.origin.scope, "myfunc")
        # Default policy expands the first frame fully.
        self.assertEqual(first_trace.code, ["040: pass"])
        self.assertIn("myfunc(", first_trace.call)
        self.assertIn("x=1", first_trace.call)
        return

    def test_create_with_no_frames(self) -> None:
        """
            Verifies the function handles an empty frame list cleanly.

            :returns: ``None``
        """
        with mock.patch.object(xtraceback, "collect_stack_frames", return_value=[]):
            ex_inst = RuntimeError("nothing here")
            tb_detail = xtraceback.create_traceback_detail(ex_inst)

        self.assertEqual(tb_detail.extype, "RuntimeError")
        self.assertEqual(tb_detail.traces, [])
        return

    def test_create_respects_policy_override_hide(self) -> None:
        """
            Verifies that the global policy override switches the rendered
            policy. With Hide, the resulting trace's ``code`` should be empty.

            :returns: ``None``
        """
        frame_detail = xtraceback.FrameDetail(
            name="myfunc",
            line_no=42,
            line_code="raise ValueError('oops')",
            filename="synthetic.py",
            co_module=None,
            co_code=None,
            args={},
            first_line=40,
            last_line=45,
            code_lines=["040: pass"]
        )

        prev_override = xtraceback.TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE
        xtraceback.TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE = xtraceback.TracebackFormatPolicy.Hide
        try:
            with mock.patch.object(
                xtraceback,
                "collect_stack_frames",
                return_value=[frame_detail]
            ):
                ex_inst = ValueError("oops")
                tb_detail = xtraceback.create_traceback_detail(ex_inst)
        finally:
            xtraceback.TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE = prev_override

        first_trace = tb_detail.traces[0]
        self.assertEqual(first_trace.code, [])
        return


class TestFormatExcLines(unittest.TestCase):
    """
        Verifies :func:`format_exc_lines` returns a list of lines.
    """

    def test_format_exc_lines_returns_list(self) -> None:
        """
            Verifies the helper returns a list when called inside an except
            block.

            :returns: ``None``
        """
        captured = None
        try:
            raise ValueError("hello")
        except ValueError:
            captured = xtraceback.format_exc_lines()
        is_list = isinstance(captured, list)
        self.assertTrue(is_list)
        self.assertGreater(len(captured), 0)
        return


class TestFormatException(unittest.TestCase):
    """
        Verifies :func:`format_exception` returns a list of formatted lines.
    """

    def test_format_exception_returns_lines(self) -> None:
        """
            Verifies the helper returns a non-empty list of strings.

            :returns: ``None``
        """
        with mock.patch.object(xtraceback, "collect_stack_frames", return_value=[]):
            ex_inst = RuntimeError("boom")
            lines = xtraceback.format_exception(ex_inst)
        is_list = isinstance(lines, list)
        self.assertTrue(is_list)
        joined = os.linesep.join(lines)
        self.assertIn("RuntimeError", joined)
        return


class TestEnhanceException(unittest.TestCase):
    """
        Verifies :func:`enhance_exception` augments an exception with context.

        Context is attached to the exception *instance* (its ``_contexts``
        mapping), keyed by the function scope that called
        :func:`enhance_exception`.  The exception's class is never modified, so
        this works for builtin exception types as well as user-defined ones.
        Attached context is read back with :func:`get_contexts`.
    """

    def test_enhance_attaches_context(self) -> None:
        """
            Verifies that calling :func:`enhance_exception` results in the
            exception carrying a context entry that includes the content,
            readable via :func:`get_contexts`.

            :returns: ``None``
        """
        class MyOpError(RuntimeError):
            pass

        def helper(xcpt: BaseException) -> None:
            xtraceback.enhance_exception(xcpt=xcpt, content="extra info", label="HINT")
            return

        ex = MyOpError("oops")
        helper(xcpt=ex)

        contexts = xtraceback.get_contexts(ex)
        is_dict = isinstance(contexts, dict)
        self.assertTrue(is_dict)
        is_present = "helper" in contexts
        self.assertTrue(is_present)
        recorded = contexts["helper"]
        self.assertEqual(recorded["label"], "HINT")
        self.assertEqual(recorded["content"], "extra info")
        return

    def test_enhance_does_not_mutate_exception_class(self) -> None:
        """
            Verifies that :func:`enhance_exception` does NOT add the mixin to
            the exception type's bases (the prior implementation mutated the
            class process-wide, breaking other instances and builtin types).

            :returns: ``None``
        """
        class IsolatedError(RuntimeError):
            pass

        bases_before = tuple(IsolatedError.__bases__)
        ex = IsolatedError("oops")
        xtraceback.enhance_exception(xcpt=ex, content="data", label="X")

        self.assertEqual(tuple(IsolatedError.__bases__), bases_before)
        self.assertNotIn(xtraceback.EnhancedErrorMixIn, IsolatedError.__bases__)

        # A second, never-enhanced instance of the same class is unaffected and
        # carries no context (the prior process-wide mutation broke this).
        other = IsolatedError("other")
        self.assertEqual(len(xtraceback.get_contexts(other)), 0)
        return

    def test_enhance_works_on_builtin_exception(self) -> None:
        """
            Verifies that :func:`enhance_exception` succeeds on builtin
            exception types (``ValueError``, ``KeyError``, ``OSError``) without
            raising ``TypeError`` — the prior implementation crashed trying to
            mutate the immutable builtin class.

            :returns: ``None``
        """
        for builtin_factory in (lambda: ValueError("v"), lambda: KeyError("k"), lambda: OSError("o")):
            ex = builtin_factory()
            xtraceback.enhance_exception(xcpt=ex, content="ctx for builtin", label="B")
            contexts = xtraceback.get_contexts(ex)
            is_present = "test_enhance_works_on_builtin_exception" in contexts
            self.assertTrue(is_present)
            self.assertEqual(contexts["test_enhance_works_on_builtin_exception"]["content"], "ctx for builtin")
        return

    def test_enhance_default_label(self) -> None:
        """
            Verifies that the default label is ``"CONTEXT"`` when not specified.

            :returns: ``None``
        """
        class AnotherOpError(RuntimeError):
            pass

        def helper(xcpt: BaseException) -> None:
            xtraceback.enhance_exception(xcpt=xcpt, content="more info")
            return

        ex = AnotherOpError("oops")
        helper(xcpt=ex)

        contexts = xtraceback.get_contexts(ex)
        is_present = "helper" in contexts
        self.assertTrue(is_present)
        recorded = contexts["helper"]
        self.assertEqual(recorded["label"], "CONTEXT")
        return

    def test_get_contexts_empty_for_unenhanced(self) -> None:
        """
            Verifies that :func:`get_contexts` returns an empty mapping for an
            exception that was never enhanced.

            :returns: ``None``
        """
        ex = RuntimeError("plain")
        contexts = xtraceback.get_contexts(ex)
        self.assertIsInstance(contexts, dict)
        self.assertEqual(len(contexts), 0)
        return


class TestRealStackWalk(unittest.TestCase):
    """
        Exercises the flagship traceback path against a *real* raised exception
        and a *real* stack walk (no mocking of ``collect_stack_frames``).  These
        tests close the gap where the prior suite mocked the stack walker and
        therefore masked the enhance/context defects.
    """

    def _raise_and_capture(self) -> BaseException:
        """
            Raises a real exception from a real function and returns the caught
            instance (with a populated ``__traceback__``).

            :returns: The caught exception instance.
        """
        captured: BaseException = RuntimeError("unset")
        try:
            raise ValueError("real boom")
        except ValueError as err:
            captured = err
        return captured

    def test_collect_stack_frames_real_walk(self) -> None:
        """
            Verifies :func:`collect_stack_frames` returns real frame details for
            a genuine exception without raising.

            :returns: ``None``
        """
        ex = self._raise_and_capture()
        frames = xtraceback.collect_stack_frames(inspect.currentframe(), ex)
        self.assertIsInstance(frames, list)
        self.assertGreater(len(frames), 0)
        scopes = [fd.name for fd in frames]
        # The raise site (from the exception's own traceback) is always present.
        self.assertIn("_raise_and_capture", scopes)
        return

    def test_format_exception_real_walk_includes_code(self) -> None:
        """
            Verifies :func:`format_exception` produces a real traceback with
            expanded source code lines for a genuine exception.

            :returns: ``None``
        """
        ex = self._raise_and_capture()
        lines = xtraceback.format_exception(ex)
        joined = os.linesep.join(lines)
        self.assertIn("ValueError", joined)
        self.assertIn("real boom", joined)
        # The first frame is expanded by default policy, so real source lines
        # from this test module appear (numbered).
        self.assertIn("raise ValueError", joined)
        return

    def test_enhanced_context_renders_in_real_traceback(self) -> None:
        """
            End-to-end: enhance a real exception with context, then verify the
            context label/content actually appear in the formatted traceback.
            This is the headline "rich contextual errors" capability that was
            previously stored but never rendered.

            :returns: ``None``
        """
        ex = self._raise_and_capture()
        xtraceback.enhance_exception(xcpt=ex, content="db connection was closed", label="HINT")

        lines = xtraceback.format_exception(ex)
        joined = os.linesep.join(lines)

        self.assertIn("HINT:", joined)
        self.assertIn("db connection was closed", joined)
        return


if __name__ == "__main__":
    unittest.main()
