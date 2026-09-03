"""
    .. module:: exceptions
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module which contains exceptions not provided by the standard python libraries.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Code Craft AI LLC"
__credits__ = []


from typing import Optional

from http.client import HTTPException


class AbstractMethodError(RuntimeError):
    """
        This error is raised when an abstract method has been called.
    """


class CancelledError(RuntimeError):
    """
        This error indicates that a operation or run is being cancelled.
    """


class CommandError(RuntimeError):
    """
        This error is the base error for command results errors.
    """
    def __init__(self, message, status, stdout, stderr, *args, **kwargs):
        """
            Initializes the :class:`CommandError` instance.

            :param message: The message describing the command failure.
            :param status: The exit status code returned by the command.
            :param stdout: The standard output captured from the command.
            :param stderr: The standard error captured from the command.

            :returns: ``None``
        """
        super().__init__(message, *args, **kwargs)
        self.status = status
        self.stdout = stdout
        self.stderr = stderr
        return


class CheckinError(RuntimeError):
    """
        This error is raised when an error occurs during the checking in of a resource.
    """

class CheckoutError(RuntimeError):
    """
        This error is raised when an error occurs during the checkout of a resource.
    """

class ConfigurationError(BaseException):
    """
        The base error object for errors that indicate that there is an issue related
        to improper configuration.

        MEANING: the code was given incorrect information that it cannot rely on in
        order to run.  The process was kicked off with wrong or corrupt input, so
        continuing would produce results derived from information already known to be
        untrustworthy.

        DO NOT CHANGE THIS BASE CLASS.  It derives from :class:`BaseException` on
        purpose so that it passes through every ``except Exception`` handler and ends
        the run no matter how much intervening code is catching broadly.  Deriving it
        from :class:`Exception` would let ordinary handlers swallow it.

        DO NOT CATCH IT.  Do not catch, suppress, or re-raise it as an
        :class:`Exception` subclass.  Downgrading it into a catchable error hands a
        later ``except Exception`` the chance to continue, and the *subsequent* error
        that then occurs usually carries no information about this original cause --
        the real problem ends up hidden behind noise.  Detect configuration problems
        as early as possible and let them stop the run.

        The one sanctioned pattern is aggregation *that still terminates*: a schema
        or spec validator may collect several configuration problems and raise a
        single ``ConfigurationError`` enumerating all of them, so the operator can
        fix them in one pass.  The run must still end with a ``ConfigurationError``.
    """

class HaltError(RuntimeError):
    """
        This error is raised when a descendant flow control context encounters an issue and exits asking
        the parent flow control to halt its progress.
    """

class InvalidConfigurationError(ConfigurationError):
    """
        This error is raised when an IntegrationCoupling object has been passed invalid configuration parameters.
    """

class LooperError(RuntimeError):
    """
        This error is raised when an error occurs with the use of the :class:`LooperPool` or
        :class:`Looper` objects.
    """

class LooperQueueShutdownError(LooperError):
    """
        This error is raised when work is being queued on a :class:`LooperQueue` thaat has
        been shutdown and when a worker thread is attempting to wait for work on an empty
        queue.
    """

class MissingConfigurationError(ConfigurationError):
    """
        This error is raised when an IntegrationCoupling object is missing required configuration parameters.
    """

class NotSupportedError(RuntimeError):
    """
        This error is raised when a method that must be overloaded has not been overridden.
    """

class PublishError(RuntimeError):
    """
        This error is raised when the publishing of an artifact fails.
    """

class SemanticError(BaseException):
    """
        The base error object for errors that indicate that there is an issue with
        a piece of automation code and with the way the Automation Kit code is being
        utilized.

        MEANING: an API or a piece of code has detected that it is being used
        incorrectly.  Treat this with the same severity as a compile-time error --
        halt and report the condition so it can be fixed.  Do not proceed under
        false pretences.

        DO NOT CHANGE THIS BASE CLASS.  It derives from :class:`BaseException` on
        purpose so that it passes through every ``except Exception`` handler and ends
        the run no matter how much intervening code is catching broadly.  Deriving it
        from :class:`Exception` would let ordinary handlers swallow it.

        DO NOT CATCH IT.  Do not catch, suppress, or re-raise it as an
        :class:`Exception` subclass.  Misuse of an API is a definitive code defect;
        allowing it to be handled lets the defective call site keep running, and the
        *subsequent* error that then occurs usually carries no information about this
        original cause.

        The only sanctioned use of ``except SemanticError`` is the guard idiom --
        catching it purely to ``raise`` it again so that a broader ``except
        Exception`` further down the same handler chain cannot swallow it:

        .. code-block:: python

            try:
                value = some_api_call()
            except SemanticError:
                # Never swallow API misuse -- let it bubble past the broad handler.
                raise
            except Exception as xcpt:
                value = fallback()
    """

class SkipError(RuntimeError):
    """
        This error is raised when a descendant flow control context, such as a testcase, wishes to exit indicating
        that its execution is being skipped.

        The consumers of this error report the `reason` and `bug` attributes, so they are
        established here rather than left for each raising site to attach. Raising
        `SkipError("a reason")` and having the handler fail on a missing attribute
        would make the plain form of the error unusable.
    """

    def __init__(self, reason: str = "", bug: Optional[str] = None, *args):
        """
            :param reason: Why the execution is being skipped.
            :param bug: Optional identifier of the bug the skip is waiting on. A skip
                with a bug reference is temporary; one without is a condition of the
                environment, such as a credential that is not configured.
            :param args: Any further arguments, passed through to RuntimeError.
        """
        super().__init__(reason, *args)
        self.reason = reason
        self.bug = bug
        return

class TaskingCancelled(CancelledError):
    """
        The exception that is raised with a tasking is cancelled.
    """

class TaskingGroupAssertionError(AssertionError):
    """
        The exception that is raised when the only failures in a group of
        taskings are of type AssertionError.
    """

class TaskingGroupCancelled(CancelledError):
    """
        The exception that is raised when any of the taskings in a tasking
        group, completed with a cancelled error.
    """

class TaskingGroupRuntimeError(RuntimeError):
    """
        The exception that is raised when any of the taskings in a tasking group
        completed with a NON Assertion error or NON Cancellation error.
    """

class UnknownParameterError(RuntimeError):
    """
        This error is raised when the test framework encounters a
        reference to a well-known parameter that cannot be resolved.
    """

class UnSupportedPlatformError(RuntimeError):
    """
        This error is raised when the test framework encounters code that is
         not supported for the current platform environment
    """


# ===============================================================
#                  Timeout Errors
# ===============================================================

class CompletionTimeout(TimeoutError):
    """
        The exception that is raised when something has not completed within
        a constrained amount of time.
    """

class ConnectionTimeout(TimeoutError):
    """
        The exception that is raised when something has not been able to make a
        connection within a constrained amount of time.
    """

class InActivityTimeout(TimeoutError):
    """
        The exception that is raised when there has been no activity for a task
        or connection within a constrained amount of time.
    """

# ===============================================================
#                  Commandline Errors
# ===============================================================
class CommandlineError(RuntimeError):
    """
        This is the base error for all commandline utility related errors.
    """


class BadOptionUsageError(CommandlineError):
    """
        This exception is raised when an option is improperly used.
    """

    def __init__(self, message: str, parameter_name: str, hint: str):
        """
            Initializes a :class:`BadOptionUsageError` instance.

            :param message: The reason the option usage was invalid.
            :param parameter_name: The name of the affected option.
            :param hint: A string containing usage guidance.

            :returns: ``None``
        """
        super().__init__(message)
        self.parameter_name = parameter_name
        self.hint = hint
        return


class BadParameterError(CommandlineError):
    """
        Raised when an option or argument are passed with a bad value.
    """

    def __init__(self, message: str, parameter_name: str, hint: str):
        """
            Initializes a :class:`BadParameterError` instance.

            :param message: The error text describing the invalid value.
            :param parameter_name: The name of the parameter that was invalid.
            :param hint: A string containing usage guidance.

            :returns: ``None``
        """
        super().__init__(message)
        self.parameter_name = parameter_name
        self.hint = hint
        return


class MissingArgumentError(CommandlineError):
    """
        Raised when a command is missing a required argument.
    """

    def __init__(self, message: str, argument_name: str, argument_type: str, hint: str):
        """
            Initializes a :class:`MissingArgumentError` instance.

            :param message: The reason the argument is required.
            :param argument_name: The name of the missing argument.
            :param argument_type: The expected type for the argument.
            :param hint: Guidance for supplying the argument.

            :returns: ``None``
        """
        super().__init__(message)
        self.argument_name = argument_name
        self.argument_type = argument_type
        self.hint = hint
        return


class MissingOptionError(CommandlineError):
    """
        Raised when a command is missing a required option.
    """

    def __init__(self, message: str, option_name: str, option_type: str, hint: str):
        """
            Initializes a :class:`MissingOptionError` instance.

            :param message: The message describing the missing option.
            :param option_name: The name of the required option.
            :param option_type: The expected type for the option value.
            :param hint: Guidance for supplying the option.

            :returns: ``None``
        """
        super().__init__(message)
        self.option_name = option_name
        self.option_type = option_type
        self.hint = hint
        return


class NoSuchOptionError(CommandlineError):
    """
        Raised when a un-recognized flag was passed on the commandline for a given command.
    """

    def __init__(self, message: str, flag: str):
        """
            Initializes a :class:`NoSuchOptionError` instance.

            :param message: Explanation for the unknown option.
            :param flag: The flag value that was not recognized.

            :returns: ``None``
        """
        super().__init__(message)
        self.flag = flag
        return

class TooManyArgumentsError(CommandlineError):
    """
        Raised with too many arguments were passed on the commandline for a given command.
    """

    def __init__(self, message):
        """
            Initializes a :class:`TooManyArgumentsError` instance.

            :param message: The message describing the extraneous arguments.

            :returns: ``None``
        """
        super().__init__(message)
        return

# ===============================================================
#                  Protocol Errors
# ===============================================================
class ProtocolError(RuntimeError):
    """
        This error is raised when a communications protocol encounters an error.
    """

class UnExpectedSessionClosureError(RuntimeError):
    """
        This error is raised when a protocol session is unexpectedly closed.
    """

class HTTPRequestError(HTTPException):
    """
        This error is raised when a HTTP request encounters an error.
    """


# ===============================================================
# Sorted by status code
# ===============================================================

# --------------- 3xx Status Code Errors-----------------

class HttpResponse3xxError(HTTPException):
    """
        The base exception type for all the 3xx class of HTTP exceptions.
    """

class HttpRedirectMultipleChoicesError(HttpResponse3xxError):
    """
        Raise when the HTTPStatus.300 status code is received and not handled.
    """

class HttpRedirectMovedPermanentlyError(HttpResponse3xxError):
    """
        Raise when the HTTPStatus.301 status code is received and not handled.
    """
class HttpRedirectMovedTemporarilyError(HttpResponse3xxError):
    """
        Raise when the HTTPStatus.302 status code is received and not handled.
    """

class HttpRedirectSeeOtherError(HttpResponse3xxError):
    """
        Raise when the HTTPStatus.303 status code is received and not handled.
    """

class HttpRedirectNotModifiedError(HttpResponse3xxError):
    """
        Raise when the HTTPStatus.304 status code is received and not handled.
    """

class HttpRedirectUseProxyError(HttpResponse3xxError):
    """
        Raise when the HTTPStatus.305 status code is received and not handled.
    """

class HttpRedirectSwitchProxyError(HttpResponse3xxError):
    """
        Raise when the HTTPStatus.306 status code is received and not handled.
    """

class HttpRedirectTemporaryError(HttpResponse3xxError):
    """
        Raise when the HTTPStatus.307 status code is received and not handled.
    """

class HttpRedirectPermanentError(HttpResponse3xxError):
    """
        Raise when the HTTPStatus.308 status code is received and not handled.
    """

# --------------- 4xx Status Code Errors-----------------

class HttpResponse4xxError(HTTPException):
    """
        The base exception type for all the 3xx class of HTTP exceptions.
    """

class HttpBadRequestError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.400 status code is received.
    """

class HttpUnAuthorizedError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.401 status code is received.
    """

class HttpPaymentRequiredError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.402 status code is received.
    """

class HttpForbiddenError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.403 status code is received.
    """

class HttpNotFoundError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.404 status code is received.
    """

class HttpMethodNotAllowedError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.405 status code is received.
    """

class HttpNotAcceptableError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.406 status code is received.
    """

class HttpProxyAuthenticationRequiredError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.407 status code is received.
    """

class HttpRequestTimeoutError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.408 status code is received.
    """

class HttpConflictError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.409 status code is received.
    """

class HttpGoneError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.410 status code is received.
    """

class HttpLengthRequiredError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.411 status code is received.
    """

class HttpPreConditionFailedError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.412 status code is received.
    """

class HttpPayloadTooLargeError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.413 status code is received.
    """

class HttpUriTooLongError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.414 status code is received.
    """

class HttpUnSupportedMediaTypeError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.415 status code is received.
    """

class HttpRangeNotSatisfiableError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.416 status code is received.
    """

class HttpExpectationFailedError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.417 status code is received.
    """

class HttpImATeapotError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.418 status code is received.
    """

class HttpMisdirectedRequestError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.421 status code is received.
    """

class HttpUnprocessableContentError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.422 status code is received.
    """

class HttpLockedError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.423 status code is received.
    """

class HttpFailedDependencyError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.424 status code is received.
    """

class HttpTooEarlyError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.425 status code is received.
    """

class HttpUpgradeRequiredError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.426 status code is received.
    """

class HttpPreconditionRequiredError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.428 status code is received.
    """

class HttpTooManyRequestsError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.429 status code is received.
    """

class HttpHeaderFieldsTooLargeError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.431 status code is received.
    """

class HttpUnavailableForLegalReasonsError(HttpResponse4xxError):
    """
        Raised when the HTTPStatus.451 status code is received.
    """

# --------------- 5xx Status Code Errors-----------------


class HttpResponse5xxError(HTTPException):
    """
        The base exception type for all the 5xx class of HTTP exceptions.
    """

class HttpInternalServerError(HttpResponse5xxError):
    """
        Raised when the HTTPStatus.500 status code is received.
    """

class HttpNotImplementedError(HttpResponse5xxError):
    """
        Raised when the HTTPStatus.501 status code is received.
    """

class HttpBadGatewayError(HttpResponse5xxError):
    """
        Raised when the HTTPStatus.502 status code is received.
    """

class HttpServiceUnavailableError(HttpResponse5xxError):
    """
        Raised when the HTTPStatus.503 status code is received.
    """

class HttpGatewayTimeoutError(HttpResponse5xxError):
    """
        Raised when the HTTPStatus.504 status code is received.
    """

class HttpVersionNotSupportedError(HttpResponse5xxError):
    """
        Raised when the HTTPStatus.505 status code is received.
    """

class HttpCircularReferenceError(HttpResponse5xxError):
    """
        Raised when the HTTPStatus.506 status code is received.
    """

class HttpInsufficientStorageError(HttpResponse5xxError):
    """
        Raised when the HTTPStatus.507 status code is received.
    """

class HttpLoopDetectedError(HttpResponse5xxError):
    """
        Raised when the HTTPStatus.508 status code is received.
    """

class HttpNotExtendedError(HttpResponse5xxError):
    """
        Raised when the HTTPStatus.510 status code is received.
    """

class HttpNetworkAuthenticationRequiredError(HttpResponse5xxError):
    """
        Raised when the HTTPStatus.511 status code is received.
    """

class HttpOtherCodeError(HTTPException):
    """
        Can be raised when a HTTP Status code is recieved that is of an unknow value.
    """