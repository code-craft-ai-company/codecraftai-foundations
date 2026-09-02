"""
    .. module:: test_exceptions
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Unit tests covering the exception classes defined in
                   :mod:`ccai.errors.exceptions`.

    .. moduleauthor:: Code Craft AI
"""

import unittest

from http.client import HTTPException

from ccai.errors import exceptions


class TestSimpleRuntimeErrors(unittest.TestCase):
    """
        Verifies that simple ``RuntimeError`` subclasses retain the right
        inheritance and propagate their message argument.
    """

    def test_abstract_method_error_inherits_runtime_error(self) -> None:
        """
            Verifies :class:`AbstractMethodError` is a subclass of
            :class:`RuntimeError`.

            :returns: ``None``
        """
        is_runtime = issubclass(exceptions.AbstractMethodError, RuntimeError)
        self.assertTrue(is_runtime)
        return

    def test_cancelled_error_inherits_runtime_error(self) -> None:
        """
            Verifies :class:`CancelledError` is a subclass of :class:`RuntimeError`.

            :returns: ``None``
        """
        is_runtime = issubclass(exceptions.CancelledError, RuntimeError)
        self.assertTrue(is_runtime)
        return

    def test_simple_runtime_subclass_message(self) -> None:
        """
            Verifies that the simple runtime subclasses preserve their
            constructor message argument.

            :returns: ``None``
        """
        msg = "boom"
        inst = exceptions.AbstractMethodError(msg)
        self.assertEqual(str(inst), msg)
        return

    def test_halt_error_inherits_runtime_error(self) -> None:
        """
            Verifies :class:`HaltError` is a subclass of :class:`RuntimeError`.

            :returns: ``None``
        """
        is_runtime = issubclass(exceptions.HaltError, RuntimeError)
        self.assertTrue(is_runtime)
        return

    def test_skip_error_inherits_runtime_error(self) -> None:
        """
            Verifies :class:`SkipError` is a subclass of :class:`RuntimeError`.

            :returns: ``None``
        """
        is_runtime = issubclass(exceptions.SkipError, RuntimeError)
        self.assertTrue(is_runtime)
        return

    def test_publish_error_inherits_runtime_error(self) -> None:
        """
            Verifies :class:`PublishError` is a subclass of :class:`RuntimeError`.

            :returns: ``None``
        """
        is_runtime = issubclass(exceptions.PublishError, RuntimeError)
        self.assertTrue(is_runtime)
        return

    def test_not_supported_error_inherits_runtime_error(self) -> None:
        """
            Verifies :class:`NotSupportedError` is a subclass of :class:`RuntimeError`.

            :returns: ``None``
        """
        is_runtime = issubclass(exceptions.NotSupportedError, RuntimeError)
        self.assertTrue(is_runtime)
        return

    def test_unknown_parameter_error_inherits_runtime_error(self) -> None:
        """
            Verifies :class:`UnknownParameterError` is a subclass of :class:`RuntimeError`.

            :returns: ``None``
        """
        is_runtime = issubclass(exceptions.UnknownParameterError, RuntimeError)
        self.assertTrue(is_runtime)
        return

    def test_unsupported_platform_error_inherits_runtime_error(self) -> None:
        """
            Verifies :class:`UnSupportedPlatformError` is a subclass of :class:`RuntimeError`.

            :returns: ``None``
        """
        is_runtime = issubclass(exceptions.UnSupportedPlatformError, RuntimeError)
        self.assertTrue(is_runtime)
        return

    def test_checkin_error_inherits_runtime_error(self) -> None:
        """
            Verifies :class:`CheckinError` is a subclass of :class:`RuntimeError`.

            :returns: ``None``
        """
        is_runtime = issubclass(exceptions.CheckinError, RuntimeError)
        self.assertTrue(is_runtime)
        return

    def test_checkout_error_inherits_runtime_error(self) -> None:
        """
            Verifies :class:`CheckoutError` is a subclass of :class:`RuntimeError`.

            :returns: ``None``
        """
        is_runtime = issubclass(exceptions.CheckoutError, RuntimeError)
        self.assertTrue(is_runtime)
        return


class TestCommandError(unittest.TestCase):
    """
        Verifies the constructor and attributes of :class:`CommandError`.
    """

    def test_command_error_inherits_runtime_error(self) -> None:
        """
            Verifies :class:`CommandError` is a subclass of :class:`RuntimeError`.

            :returns: ``None``
        """
        is_runtime = issubclass(exceptions.CommandError, RuntimeError)
        self.assertTrue(is_runtime)
        return

    def test_command_error_attributes(self) -> None:
        """
            Verifies :class:`CommandError` records the supplied attributes.

            :returns: ``None``
        """
        msg = "command failed"
        status = 7
        stdout = "out"
        stderr = "err"
        inst = exceptions.CommandError(msg, status, stdout, stderr)
        self.assertEqual(inst.status, status)
        self.assertEqual(inst.stdout, stdout)
        self.assertEqual(inst.stderr, stderr)
        self.assertIn(msg, inst.args)
        return

    def test_command_error_with_extra_args(self) -> None:
        """
            Verifies :class:`CommandError` propagates extra positional args.

            :returns: ``None``
        """
        msg = "failed"
        extra = "extra"
        inst = exceptions.CommandError(msg, 1, "", "", extra)
        self.assertIn(extra, inst.args)
        return

    def test_command_error_empty_streams(self) -> None:
        """
            Verifies :class:`CommandError` accepts empty stdout and stderr.

            :returns: ``None``
        """
        inst = exceptions.CommandError("msg", 0, "", "")
        self.assertEqual(inst.stdout, "")
        self.assertEqual(inst.stderr, "")
        return


class TestSemanticError(unittest.TestCase):
    """
        Verifies the special-case :class:`SemanticError`.

        Per coding standards, :class:`SemanticError` must NEVER be caught and
        must be a top-level class derived directly from :class:`BaseException`
        so that it bypasses bare ``except Exception:`` blocks.
    """

    def test_semantic_error_is_top_level(self) -> None:
        """
            Verifies :class:`SemanticError` is a direct subclass of :class:`BaseException`
            and is NOT a subclass of :class:`Exception`.

            :returns: ``None``
        """
        is_base = issubclass(exceptions.SemanticError, BaseException)
        self.assertTrue(is_base)
        is_exc_subclass = issubclass(exceptions.SemanticError, Exception)
        self.assertFalse(is_exc_subclass)
        return

    def test_semantic_error_not_caught_by_except_exception(self) -> None:
        """
            Verifies that :class:`SemanticError` bypasses ``except Exception:``
            handlers.

            :returns: ``None``
        """
        msg = "should bubble"
        caught = False
        try:
            try:
                raise exceptions.SemanticError(msg)
            except Exception:
                caught = True
        except exceptions.SemanticError:
            pass
        self.assertFalse(caught)
        return

    def test_semantic_error_message(self) -> None:
        """
            Verifies the constructor preserves a message argument.

            :returns: ``None``
        """
        msg = "bad usage"
        inst = exceptions.SemanticError(msg)
        self.assertEqual(str(inst), msg)
        return


class TestConfigurationErrors(unittest.TestCase):
    """
        Verifies the :class:`ConfigurationError` hierarchy.
    """

    def test_configuration_error_is_top_level(self) -> None:
        """
            Verifies :class:`ConfigurationError` is a direct subclass of
            :class:`BaseException`.

            :returns: ``None``
        """
        is_base = issubclass(exceptions.ConfigurationError, BaseException)
        self.assertTrue(is_base)
        is_exc = issubclass(exceptions.ConfigurationError, Exception)
        self.assertFalse(is_exc)
        return

    def test_invalid_configuration_error_inheritance(self) -> None:
        """
            Verifies :class:`InvalidConfigurationError` extends :class:`ConfigurationError`.

            :returns: ``None``
        """
        is_config = issubclass(exceptions.InvalidConfigurationError, exceptions.ConfigurationError)
        self.assertTrue(is_config)
        return

    def test_missing_configuration_error_inheritance(self) -> None:
        """
            Verifies :class:`MissingConfigurationError` extends :class:`ConfigurationError`.

            :returns: ``None``
        """
        is_config = issubclass(exceptions.MissingConfigurationError, exceptions.ConfigurationError)
        self.assertTrue(is_config)
        return


class TestLooperErrors(unittest.TestCase):
    """
        Verifies the :class:`LooperError` hierarchy.
    """

    def test_looper_error_inheritance(self) -> None:
        """
            Verifies :class:`LooperError` is a subclass of :class:`RuntimeError`.

            :returns: ``None``
        """
        is_runtime = issubclass(exceptions.LooperError, RuntimeError)
        self.assertTrue(is_runtime)
        return

    def test_looper_queue_shutdown_error_inheritance(self) -> None:
        """
            Verifies :class:`LooperQueueShutdownError` is a subclass of
            :class:`LooperError`.

            :returns: ``None``
        """
        is_looper = issubclass(exceptions.LooperQueueShutdownError, exceptions.LooperError)
        self.assertTrue(is_looper)
        return


class TestTaskingErrors(unittest.TestCase):
    """
        Verifies the tasking-related error hierarchy.
    """

    def test_tasking_cancelled_inheritance(self) -> None:
        """
            Verifies :class:`TaskingCancelled` extends :class:`CancelledError`.

            :returns: ``None``
        """
        is_cancelled = issubclass(exceptions.TaskingCancelled, exceptions.CancelledError)
        self.assertTrue(is_cancelled)
        return

    def test_tasking_group_cancelled_inheritance(self) -> None:
        """
            Verifies :class:`TaskingGroupCancelled` extends :class:`CancelledError`.

            :returns: ``None``
        """
        is_cancelled = issubclass(exceptions.TaskingGroupCancelled, exceptions.CancelledError)
        self.assertTrue(is_cancelled)
        return

    def test_tasking_group_assertion_error_inheritance(self) -> None:
        """
            Verifies :class:`TaskingGroupAssertionError` extends :class:`AssertionError`.

            :returns: ``None``
        """
        is_assertion = issubclass(exceptions.TaskingGroupAssertionError, AssertionError)
        self.assertTrue(is_assertion)
        return

    def test_tasking_group_runtime_error_inheritance(self) -> None:
        """
            Verifies :class:`TaskingGroupRuntimeError` extends :class:`RuntimeError`.

            :returns: ``None``
        """
        is_runtime = issubclass(exceptions.TaskingGroupRuntimeError, RuntimeError)
        self.assertTrue(is_runtime)
        return


class TestTimeoutErrors(unittest.TestCase):
    """
        Verifies the timeout-related error hierarchy.
    """

    def test_completion_timeout_inheritance(self) -> None:
        """
            Verifies :class:`CompletionTimeout` extends :class:`TimeoutError`.

            :returns: ``None``
        """
        is_timeout = issubclass(exceptions.CompletionTimeout, TimeoutError)
        self.assertTrue(is_timeout)
        return

    def test_connection_timeout_inheritance(self) -> None:
        """
            Verifies :class:`ConnectionTimeout` extends :class:`TimeoutError`.

            :returns: ``None``
        """
        is_timeout = issubclass(exceptions.ConnectionTimeout, TimeoutError)
        self.assertTrue(is_timeout)
        return

    def test_inactivity_timeout_inheritance(self) -> None:
        """
            Verifies :class:`InActivityTimeout` extends :class:`TimeoutError`.

            :returns: ``None``
        """
        is_timeout = issubclass(exceptions.InActivityTimeout, TimeoutError)
        self.assertTrue(is_timeout)
        return


class TestCommandlineErrors(unittest.TestCase):
    """
        Verifies the :class:`CommandlineError` hierarchy and attribute storage.
    """

    def test_commandline_error_inheritance(self) -> None:
        """
            Verifies :class:`CommandlineError` extends :class:`RuntimeError`.

            :returns: ``None``
        """
        is_runtime = issubclass(exceptions.CommandlineError, RuntimeError)
        self.assertTrue(is_runtime)
        return

    def test_bad_option_usage_error_attributes(self) -> None:
        """
            Verifies :class:`BadOptionUsageError` records the supplied attributes.

            :returns: ``None``
        """
        msg = "invalid usage"
        param = "--config"
        hint = "specify a path"
        inst = exceptions.BadOptionUsageError(msg, param, hint)
        self.assertEqual(inst.parameter_name, param)
        self.assertEqual(inst.hint, hint)
        is_cmdline = isinstance(inst, exceptions.CommandlineError)
        self.assertTrue(is_cmdline)
        return

    def test_bad_parameter_error_attributes(self) -> None:
        """
            Verifies :class:`BadParameterError` records the supplied attributes.

            :returns: ``None``
        """
        msg = "bad value"
        param = "--count"
        hint = "must be an integer"
        inst = exceptions.BadParameterError(msg, param, hint)
        self.assertEqual(inst.parameter_name, param)
        self.assertEqual(inst.hint, hint)
        is_cmdline = isinstance(inst, exceptions.CommandlineError)
        self.assertTrue(is_cmdline)
        return

    def test_missing_argument_error_attributes(self) -> None:
        """
            Verifies :class:`MissingArgumentError` records the supplied attributes.

            :returns: ``None``
        """
        msg = "missing arg"
        argument_name = "input"
        argument_type = "PATH"
        hint = "provide the input file"
        inst = exceptions.MissingArgumentError(msg, argument_name, argument_type, hint)
        self.assertEqual(inst.argument_name, argument_name)
        self.assertEqual(inst.argument_type, argument_type)
        self.assertEqual(inst.hint, hint)
        return

    def test_missing_option_error_attributes(self) -> None:
        """
            Verifies :class:`MissingOptionError` records the supplied attributes.

            :returns: ``None``
        """
        msg = "missing option"
        option_name = "--output"
        option_type = "PATH"
        hint = "specify the output file"
        inst = exceptions.MissingOptionError(msg, option_name, option_type, hint)
        self.assertEqual(inst.option_name, option_name)
        self.assertEqual(inst.option_type, option_type)
        self.assertEqual(inst.hint, hint)
        return

    def test_no_such_option_error_attributes(self) -> None:
        """
            Verifies :class:`NoSuchOptionError` records the supplied flag.

            :returns: ``None``
        """
        msg = "unknown flag"
        flag = "--bogus"
        inst = exceptions.NoSuchOptionError(msg, flag)
        self.assertEqual(inst.flag, flag)
        is_cmdline = isinstance(inst, exceptions.CommandlineError)
        self.assertTrue(is_cmdline)
        return

    def test_too_many_arguments_error_message(self) -> None:
        """
            Verifies :class:`TooManyArgumentsError` preserves its message.

            :returns: ``None``
        """
        msg = "too many"
        inst = exceptions.TooManyArgumentsError(msg)
        self.assertEqual(str(inst), msg)
        is_cmdline = isinstance(inst, exceptions.CommandlineError)
        self.assertTrue(is_cmdline)
        return


class TestProtocolErrors(unittest.TestCase):
    """
        Verifies the protocol-related error hierarchy.
    """

    def test_protocol_error_inheritance(self) -> None:
        """
            Verifies :class:`ProtocolError` extends :class:`RuntimeError`.

            :returns: ``None``
        """
        is_runtime = issubclass(exceptions.ProtocolError, RuntimeError)
        self.assertTrue(is_runtime)
        return

    def test_unexpected_session_closure_error_inheritance(self) -> None:
        """
            Verifies :class:`UnExpectedSessionClosureError` extends
            :class:`RuntimeError`.

            :returns: ``None``
        """
        is_runtime = issubclass(exceptions.UnExpectedSessionClosureError, RuntimeError)
        self.assertTrue(is_runtime)
        return

    def test_http_request_error_inheritance(self) -> None:
        """
            Verifies :class:`HTTPRequestError` extends :class:`HTTPException`.

            :returns: ``None``
        """
        is_http = issubclass(exceptions.HTTPRequestError, HTTPException)
        self.assertTrue(is_http)
        return


class TestHttp3xxErrors(unittest.TestCase):
    """
        Verifies the 3xx HTTP error hierarchy.
    """

    def test_3xx_base_inheritance(self) -> None:
        """
            Verifies :class:`HttpResponse3xxError` extends :class:`HTTPException`.

            :returns: ``None``
        """
        is_http = issubclass(exceptions.HttpResponse3xxError, HTTPException)
        self.assertTrue(is_http)
        return

    def test_3xx_redirect_classes_inheritance(self) -> None:
        """
            Verifies the individual 3xx redirect classes extend
            :class:`HttpResponse3xxError`.

            :returns: ``None``
        """
        candidate_classes = [
            exceptions.HttpRedirectMultipleChoicesError,
            exceptions.HttpRedirectMovedPermanentlyError,
            exceptions.HttpRedirectMovedTemporarilyError,
            exceptions.HttpRedirectSeeOtherError,
            exceptions.HttpRedirectNotModifiedError,
            exceptions.HttpRedirectUseProxyError,
            exceptions.HttpRedirectSwitchProxyError,
            exceptions.HttpRedirectTemporaryError,
            exceptions.HttpRedirectPermanentError,
        ]
        for nxtcls in candidate_classes:
            is_3xx = issubclass(nxtcls, exceptions.HttpResponse3xxError)
            self.assertTrue(is_3xx, f"{nxtcls.__name__} should subclass HttpResponse3xxError")
        return


class TestHttp4xxErrors(unittest.TestCase):
    """
        Verifies the 4xx HTTP error hierarchy.
    """

    def test_4xx_base_inheritance(self) -> None:
        """
            Verifies :class:`HttpResponse4xxError` extends :class:`HTTPException`.

            :returns: ``None``
        """
        is_http = issubclass(exceptions.HttpResponse4xxError, HTTPException)
        self.assertTrue(is_http)
        return

    def test_common_4xx_classes_inheritance(self) -> None:
        """
            Verifies common 4xx classes extend :class:`HttpResponse4xxError`.

            :returns: ``None``
        """
        candidate_classes = [
            exceptions.HttpBadRequestError,
            exceptions.HttpUnAuthorizedError,
            exceptions.HttpForbiddenError,
            exceptions.HttpNotFoundError,
            exceptions.HttpMethodNotAllowedError,
            exceptions.HttpConflictError,
            exceptions.HttpGoneError,
            exceptions.HttpImATeapotError,
            exceptions.HttpTooManyRequestsError,
            exceptions.HttpUnavailableForLegalReasonsError,
        ]
        for nxtcls in candidate_classes:
            is_4xx = issubclass(nxtcls, exceptions.HttpResponse4xxError)
            self.assertTrue(is_4xx, f"{nxtcls.__name__} should subclass HttpResponse4xxError")
        return


class TestHttp5xxErrors(unittest.TestCase):
    """
        Verifies the 5xx HTTP error hierarchy.
    """

    def test_5xx_base_inheritance(self) -> None:
        """
            Verifies :class:`HttpResponse5xxError` extends :class:`HTTPException`.

            :returns: ``None``
        """
        is_http = issubclass(exceptions.HttpResponse5xxError, HTTPException)
        self.assertTrue(is_http)
        return

    def test_common_5xx_classes_inheritance(self) -> None:
        """
            Verifies common 5xx classes extend :class:`HttpResponse5xxError`.

            :returns: ``None``
        """
        candidate_classes = [
            exceptions.HttpInternalServerError,
            exceptions.HttpNotImplementedError,
            exceptions.HttpBadGatewayError,
            exceptions.HttpServiceUnavailableError,
            exceptions.HttpGatewayTimeoutError,
            exceptions.HttpVersionNotSupportedError,
            exceptions.HttpInsufficientStorageError,
            exceptions.HttpLoopDetectedError,
            exceptions.HttpNotExtendedError,
            exceptions.HttpNetworkAuthenticationRequiredError,
        ]
        for nxtcls in candidate_classes:
            is_5xx = issubclass(nxtcls, exceptions.HttpResponse5xxError)
            self.assertTrue(is_5xx, f"{nxtcls.__name__} should subclass HttpResponse5xxError")
        return

    def test_http_other_code_error_inheritance(self) -> None:
        """
            Verifies :class:`HttpOtherCodeError` extends :class:`HTTPException`.

            :returns: ``None``
        """
        is_http = issubclass(exceptions.HttpOtherCodeError, HTTPException)
        self.assertTrue(is_http)
        return


class TestRaiseChaining(unittest.TestCase):
    """
        Verifies that exception chaining works for the more elaborate types in
        the module.
    """

    def test_command_error_with_explicit_cause(self) -> None:
        """
            Verifies :class:`CommandError` records ``__cause__`` when raised
            with the ``from`` clause.

            :returns: ``None``
        """
        original = ValueError("root")
        captured = None
        try:
            try:
                raise original
            except ValueError as ve:
                raise exceptions.CommandError("wrapped", 1, "out", "err") from ve
        except exceptions.CommandError as ce:
            captured = ce
        self.assertIsNotNone(captured)
        self.assertIs(captured.__cause__, original)
        return

    def test_command_error_without_explicit_cause(self) -> None:
        """
            Verifies that a :class:`CommandError` raised standalone has no
            ``__cause__``.

            :returns: ``None``
        """
        captured = None
        try:
            raise exceptions.CommandError("plain", 0, "", "")
        except exceptions.CommandError as ce:
            captured = ce
        self.assertIsNotNone(captured)
        self.assertIsNone(captured.__cause__)
        return


if __name__ == "__main__":
    unittest.main()
