"""
    .. module:: xtraceback
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module which contains functions for enhancing and formatting exceptions and
                   common exception types not provided by python.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Any, Dict, List, Optional

from types import ModuleType, CodeType

import inspect
import os
import re
import traceback


from collections import OrderedDict

from dataclasses import dataclass

from ccai.errors.exceptions import SemanticError



ARG_ERROR = "<error>"

DECORATOR_EXPR = re.compile(r"^[\s]*@[\D\w]{1}[\d\w]*")

MEMBER_TRACE_POLICY = "__traceback_format_policy__"


class TracebackFormatPolicy:
    Brief = "Brief"
    Full = "Full"
    Hide = "Hide"

VALID_MEMBER_TRACE_POLICY = [
    TracebackFormatPolicy.Brief,
    TracebackFormatPolicy.Full,
    TracebackFormatPolicy.Hide
]



class TRACEBACK_CONFIG:
    TRACEBACK_POLICY_OVERRIDE = None
    TRACEBACK_MAX_FULL_DISPLAY = 5
    TRACEBACK_EXPAND_FIRST_N = 1


@dataclass
class FrameDetail:
    name: str
    line_no: int
    line_code: str
    filename: str

    co_module: ModuleType
    co_code: CodeType
    
    args: Dict[str, Any]

    first_line: Optional[int] = None
    last_line: Optional[int] = None
    code_lines: Optional[List[str]] = None


@dataclass
class OriginDetail:
    file: str
    lineno: int
    scope: str


@dataclass
class TraceDetail:
    origin: OriginDetail
    call: str
    code: List[str]
    context: Optional[Dict[str, str]] = None

@dataclass
class TracebackDetail:
    extype: str
    exargs: List[str]
    traces: List[TraceDetail]


def is_field(candidate: Any) -> bool:
    """
        Determines if a object member is a field.
    """

    if inspect.ismodule(candidate):
        return False
    if inspect.isclass(candidate):
        return False
    if inspect.isfunction(candidate):
        return False
    if inspect.isgeneratorfunction(candidate):
        return False
    if inspect.isgenerator(candidate):
        return False
    if inspect.iscoroutinefunction(candidate):
        return False
    if inspect.iscoroutine(candidate):
        return False
    if inspect.isasyncgenfunction(candidate):
        return False
    if inspect.isasyncgen(candidate):
        return False
    if inspect.istraceback(candidate):
        return False
    if inspect.isframe(candidate):
        return False
    if inspect.iscode(candidate):
        return False
    if inspect.isbuiltin(candidate):
        return False
    if inspect.isroutine(candidate):
        return False
    if inspect.isabstract(candidate):
        return False
    if inspect.ismethoddescriptor(candidate):
        return False
    if inspect.isdatadescriptor(candidate):
        return False
    if inspect.isgetsetdescriptor(candidate):
        return False
    if inspect.ismemberdescriptor(candidate):
        return False

    return True


def split_and_indent_lines(msg: str, level: int, indent: int=4, pre_strip_leading: bool=True) -> List[str]:
    """
        Takes a string and splits it into multiple lines, then indents each line
        to the specified level using 'indent' spaces for each level.

        :param msg: The text content to split into lines and then indent.
        :param level: The integer level number to indent to.
        :param indent: The number of spaces to indent for each level.
        :param pre_strip_leading: Strip any leading whitesspace before indenting the lines.

        :returns: The indenting lines
    """

    # Split msg into lines keeping the line endings
    msglines = msg.splitlines(False)

    prestrip_len = len(msg)
    if pre_strip_leading:
        for nxtline in msglines:
            stripped = nxtline.lstrip()
            striplen = len(nxtline) - len(stripped)
            if striplen < prestrip_len:
                prestrip_len = striplen

    pfx = " " * (level * indent)

    indented = None
    if pre_strip_leading and prestrip_len > 0:
        indented = [pfx + nxtline[prestrip_len:] for nxtline in msglines]
    else:
        indented = [pfx + nxtline for nxtline in msglines]

    return indented


class EnhancedErrorMixIn:
    def __init__(self, *args, **kwargs):
        """
            Initializes the mixin and prepares the context store.

            :param args: Positional arguments passed to the constructor.
            :param kwargs: Keyword arguments passed to the constructor.

            :returns: ``None``
        """
        self._contexts: Dict[str, Dict[str, str]] = {}
        return

    @property
    def contexts(self) -> Dict[str, Dict[str, str]]:
        """
            Provides access to the context dictionary added via
            :meth:`add_context`.

            :returns: Mapping of function names to context information.
        """
        return self._contexts

    def add_context(self, content: str, label: str = "CONTEXT") -> None:
        """
            Adds context to an exception and associates it with the function
            scope that called this method.

            :param content: The context content to attach to the exception.
            :param label: The label to prefix the context with.

            :returns: ``None``
        """
        # Stack: [0]=_caller_scope_name, [1]=add_context, [2]=our caller.
        scope_name = _caller_scope_name(skip=2)
        attach_context(self, content=content, label=label, scope_name=scope_name)
        return


def _caller_scope_name(skip: int) -> str:
    """
        Resolves the function scope name at ``skip`` levels up the call stack.

        Guards against shallow stacks (e.g. a call made at module scope) by
        clamping to the outermost available frame instead of raising
        ``IndexError``.

        :param skip: The number of frames above :func:`_caller_scope_name` to
            inspect (this helper occupies index 0 of its own stack snapshot).

        :returns: The ``co_name`` of the resolved frame.
    """
    frames = inspect.stack()

    target_index = skip
    if target_index >= len(frames):
        target_index = len(frames) - 1

    scope_frame = frames[target_index]
    scope_name = scope_frame.frame.f_code.co_name

    return scope_name


def attach_context(xcpt: BaseException, content: str, label: str, scope_name: str) -> None:
    """
        Attaches a context entry to an exception *instance* under the given
        function scope name.

        The entry is stored on the instance's own ``_contexts`` mapping; the
        exception's class is never modified, so this works for builtin
        exception types (``ValueError``, ``KeyError``, ...) as well as for
        user-defined ones.

        :param xcpt: The exception instance to attach context to.
        :param content: The context content.
        :param label: The label to prefix the context with.
        :param scope_name: The function scope name the context is associated with.

        :returns: ``None``
    """
    contexts = getattr(xcpt, "_contexts", None)
    if contexts is None:
        contexts = {}
        try:
            setattr(xcpt, "_contexts", contexts)
        except (AttributeError, TypeError):
            # An exotic exception with __slots__ and no instance __dict__ cannot
            # carry context; there is nothing further we can do, so leave it bare.
            return

    contexts[scope_name] = {
        "label": label,
        "content": content
    }

    return


def get_contexts(xcpt: BaseException) -> Dict[str, Dict[str, str]]:
    """
        Returns the context mapping attached to an exception instance.

        This is the universal accessor: it works for exceptions enhanced via
        :func:`enhance_exception`, exceptions that statically inherit
        :class:`EnhancedErrorMixIn`, and plain exceptions that were never
        enhanced (which yield an empty mapping).

        :param xcpt: The exception instance to read context from.

        :returns: Mapping of function scope name to its context entry.
    """
    contexts = getattr(xcpt, "_contexts", None)
    if contexts is None:
        contexts = {}

    return contexts


def collect_stack_frames(calling_frame, ex_inst) -> List[FrameDetail]:
    """
        Collects the stack frames for the context around ``ex_inst``.

        :param calling_frame: The frame where collection should begin.
        :param ex_inst: The exception instance being processed.

        :returns: A list of :class:`FrameDetail` objects representing the stack.
    """

    tb_code = None
    tb_lineno = None

    context_frames = []

    for tb_frame, tb_lineno in traceback.walk_stack(calling_frame):
        context_frames.insert(0, (tb_frame, tb_lineno))
        if tb_frame.f_code.co_name == '<module>':
            break 

    context_frames.pop()

    traceback_frames = []

    for tb_frame, tb_lineno in traceback.walk_tb(ex_inst.__traceback__):
        traceback_frames.append((tb_frame, tb_lineno))

    full_stack_frames = context_frames + traceback_frames
    full_stack_frames.reverse()

    frame_details_list = []

    for tb_frame, tb_lineno in full_stack_frames:
        tb_code: CodeType = tb_frame.f_code
        co_filename: str = tb_code.co_filename
        co_name: str = tb_code.co_name
        co_arg_names = tb_code.co_varnames[:tb_code.co_argcount]
        co_argcount = tb_code.co_argcount
        co_locals = tb_frame.f_locals
        co_module: ModuleType = inspect.getmodule(tb_code)
        
        code_args = OrderedDict()
        for argidx in range(0, co_argcount):
            argname = co_arg_names[argidx]
            # We cannot count on argname always being present in co_locals at the
            # time we might be processing an exception.  It could be that it has
            # already been cleaned up because it is no longer used.
            if argname in co_locals:
                argval = co_locals[argname]
                code_args[argname] = argval
            else:
                code_args[argname] = "<not found>"

        code_lines = None
        code_startline = None
        code_lastline = None
        trace_line = "<obfuscated>"
        fmt_code_lines = []

        if co_name != "<module>" and os.path.exists(co_filename) and co_filename.endswith(".py"):
            code_lines, code_startline = inspect.getsourcelines(tb_code)
            if code_lines is not None and len(code_lines) > 0:
                code_lastline = code_startline + len(code_lines)

                fmt_len = len(str(code_lastline))

                fmt_code_lines = []
                for lidx, cline in enumerate(code_lines):
                    lineno = str(code_startline + lidx).zfill(fmt_len)
                    cline = f"{lineno}: {cline.rstrip()}"
                    fmt_code_lines.append(cline)
                
                trace_line_index = tb_lineno - code_startline
                trace_line = code_lines[trace_line_index].strip()

        fdetail = FrameDetail(co_name, tb_lineno, trace_line, co_filename, co_module, tb_code, code_args, code_startline, code_lastline, fmt_code_lines)
        frame_details_list.append(fdetail)

    return frame_details_list


def create_traceback_detail(ex_inst: BaseException) -> TracebackDetail:
    """
        Builds a :class:`TracebackDetail` from an exception instance.

        :param ex_inst: The exception instance to analyze.

        :returns: A populated :class:`TracebackDetail` object.
    """

    max_full_display = TRACEBACK_CONFIG.TRACEBACK_MAX_FULL_DISPLAY
    expand_first_n = TRACEBACK_CONFIG.TRACEBACK_EXPAND_FIRST_N

    etypename = type(ex_inst).__name__
    eargs = [repr(a) for a in ex_inst.args]
    etraces = []

    calling_frame = inspect.currentframe().f_back

    stack_frames = collect_stack_frames(calling_frame, ex_inst)

    ex_contexts = get_contexts(ex_inst)

    for frame in stack_frames:
        co_module = frame.co_module

        co_format_policy = TracebackFormatPolicy.Brief
        if expand_first_n > 0 and max_full_display > 0:
            co_format_policy = TracebackFormatPolicy.Full

        if TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE is None:
            if co_module is not None and hasattr(co_module, MEMBER_TRACE_POLICY):
                cand_format_policy = getattr(co_module, MEMBER_TRACE_POLICY)
                if cand_format_policy in VALID_MEMBER_TRACE_POLICY:
                    co_format_policy = cand_format_policy
        else:
            co_format_policy = TRACEBACK_CONFIG.TRACEBACK_POLICY_OVERRIDE

        ntorigin = OriginDetail(file=frame.filename, lineno=frame.line_no, scope=frame.name)

        nt_context = None
        if frame.name in ex_contexts:
            nt_context = ex_contexts[frame.name]

        rep_args_parts = []
        for aname, aval in frame.args.items():
            arep = ARG_ERROR

            try:
                if hasattr(aval, "moniker"):
                    arep = aval.moniker
                else:
                    try:
                        arep = repr(aval)
                    # SemanticError signals API misuse and must never be
                    # swallowed by the broad handler below -- re-raise it.
                    except SemanticError:
                        raise
                    except Exception:
                        arep = f"<{type(aval)}>"
            except SemanticError:
                # SemanticError signals API misuse and must never be silently
                # swallowed — let it bubble out of the formatter.
                raise
            except Exception:
                # We might be trying to handle a remote type or something we
                # cannot even talk to any more.  If so, just leave the representation
                # as an error
                pass

            apart = f"{aname}={arep}"
            rep_args_parts.append(apart)

        rep_args = ", ".join(rep_args_parts)

        ntcall = f"{frame.name}({rep_args})"
        ntcode = []

        if co_format_policy == TracebackFormatPolicy.Full:
            if frame.code_lines is not None:
                ntcode = frame.code_lines

                max_full_display -= 1
                expand_first_n -= 1


        nttrace = TraceDetail(origin=ntorigin, call=ntcall, code=ntcode, context=nt_context)
        etraces.append(nttrace)

    tb_detail = TracebackDetail(extype=etypename, exargs=eargs, traces=etraces)

    return tb_detail


def enhance_exception(xcpt: BaseException, content: str, label: str = "CONTEXT") -> None:
    """
        Attaches contextual information to an existing exception instance.

        The context is stored on the *instance* (its ``_contexts`` mapping),
        keyed by the function scope that called this function.  The exception's
        class is intentionally **not** modified, so this works for builtin
        exception types (``ValueError``, ``KeyError``, ``OSError``, ...) as well
        as user-defined ones, and never mutates a class for the whole process.
        Read the attached context back with :func:`get_contexts`.

        :param xcpt: The exception instance to augment.
        :param content: Additional context information to associate with the
            exception.
        :param label: A label describing the context data.

        :returns: ``None``
    """

    # Stack: [0]=_caller_scope_name, [1]=enhance_exception, [2]=our caller.
    scope_name = _caller_scope_name(skip=2)

    attach_context(xcpt, content=content, label=label, scope_name=scope_name)

    return


def format_exc_lines() -> List[str]:
    """
        Gets a 'format_exc' result and splits it into mutliple lines.

        :returns: A list of strings containing the current formatted exception.
    """
    rtn_lines = traceback.format_exc().splitlines()
    return rtn_lines


def format_exception(ex_inst: BaseException) -> List[str]:
    """
        Formats an exception into a list of traceback lines.

        :param ex_inst: The exception instance to format.

        :returns: A list of strings containing the formatted traceback.
    """

    tbdetail = create_traceback_detail(ex_inst)

    exmsg_lines = format_traceback_detail(tbdetail)

    return exmsg_lines


def format_traceback_detail(tbdetail: TracebackDetail) -> List[str]:
    """
        Creates a human readable list of lines from a traceback detail object.

        :param tbdetail: The :class:`TracebackDetail` to format.

        :returns: A list of formatted traceback lines.
    """

    detail_lines = [
        f"{tbdetail.extype}: {','.join(tbdetail.exargs)}",
        "Traceback (most recent call first):"
    ]

    ntrace: TraceDetail
    for ntrace in tbdetail.traces:

        detail_lines.append(f"  File {ntrace.origin.file}, line {ntrace.origin.lineno}, in {ntrace.origin.scope}")
        
        if len(ntrace.call) > 0:
            detail_lines.append(f"    Call {ntrace.call}")

            if len(ntrace.code) > 0:
                detail_lines.append("")

                for nline in ntrace.code:
                    detail_lines.append(f"    {nline}")

        if ntrace.context is not None:
            context_label = ntrace.context.get("label", "CONTEXT")
            context_content = ntrace.context.get("content", "")
            detail_lines.append(f"    {context_label}: {context_content}")

        detail_lines.append("")

    return detail_lines


