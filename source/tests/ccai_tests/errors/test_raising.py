"""
    .. module:: test_raising
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Unit tests covering the helpers in :mod:`automojo.errors.raising`.

    .. moduleauthor:: Automation Mojo
"""

import os
import unittest

from http.client import HTTPException

from automojo.errors import exceptions
from automojo.errors import raising


class TestFormatHttpErrorMessage(unittest.TestCase):
    """
        Verifies :func:`format_http_error_message` builds the right
        multi-line message based on the inputs.
    """

    def test_format_minimal(self) -> None:
        """
            Verifies the message format when neither ``url`` nor ``context``
            are supplied.

            :returns: ``None``
        """
        msg = raising.format_http_error_message(resp_code=404, resp_msg="Not Found")
        expected = "HTTP Error: code=404 message=Not Found."
        self.assertEqual(msg, expected)
        return

    def test_format_with_url(self) -> None:
        """
            Verifies the message format when only ``url`` is supplied.

            :returns: ``None``
        """
        msg = raising.format_http_error_message(
            resp_code=500,
            resp_msg="Internal Server Error",
            url="http://example.com/api"
        )
        expected_lines = [
            "HTTP Error: code=500 message=Internal Server Error.",
            "URL: http://example.com/api"
        ]
        expected = os.linesep.join(expected_lines)
        self.assertEqual(msg, expected)
        return

    def test_format_with_context(self) -> None:
        """
            Verifies the message format when only ``context`` is supplied.

            :returns: ``None``
        """
        msg = raising.format_http_error_message(
            resp_code=403,
            resp_msg="Forbidden",
            context="bad creds"
        )
        expected_lines = [
            "HTTP Error: code=403 message=Forbidden.",
            "CONTEXT: bad creds"
        ]
        expected = os.linesep.join(expected_lines)
        self.assertEqual(msg, expected)
        return

    def test_format_with_url_and_context(self) -> None:
        """
            Verifies the message format when both ``url`` and ``context`` are
            supplied.

            :returns: ``None``
        """
        msg = raising.format_http_error_message(
            resp_code=400,
            resp_msg="Bad Request",
            url="http://example.com/x",
            context="malformed body"
        )
        expected_lines = [
            "HTTP Error: code=400 message=Bad Request.",
            "URL: http://example.com/x",
            "CONTEXT: malformed body"
        ]
        expected = os.linesep.join(expected_lines)
        self.assertEqual(msg, expected)
        return

    def test_format_empty_message(self) -> None:
        """
            Verifies the message format gracefully handles an empty ``resp_msg``.

            :returns: ``None``
        """
        msg = raising.format_http_error_message(resp_code=204, resp_msg="")
        expected = "HTTP Error: code=204 message=."
        self.assertEqual(msg, expected)
        return

    def test_format_long_message(self) -> None:
        """
            Verifies the helper handles a very long ``resp_msg``.

            :returns: ``None``
        """
        long_msg = "A" * 5000
        msg = raising.format_http_error_message(resp_code=500, resp_msg=long_msg)
        contains_msg = long_msg in msg
        self.assertTrue(contains_msg)
        return


class TestRaiseForHttpStatus(unittest.TestCase):
    """
        Verifies :func:`raise_for_http_status` raises the right exception type
        for a wide range of status codes.
    """

    def test_success_status_does_not_raise(self) -> None:
        """
            Verifies a 2xx status code does not raise.

            :returns: ``None``
        """
        result = raising.raise_for_http_status(
            resp_code=200,
            resp_msg="OK",
            call_url="http://x",
            context=None
        )
        self.assertIsNone(result)
        return

    def test_status_below_300_does_not_raise(self) -> None:
        """
            Verifies a status of 299 does not raise.

            :returns: ``None``
        """
        result = raising.raise_for_http_status(
            resp_code=299,
            resp_msg="OK",
            call_url="http://x"
        )
        self.assertIsNone(result)
        return

    def test_known_3xx_status_raises_specific(self) -> None:
        """
            Verifies a known 3xx status raises the mapped exception type.

            :returns: ``None``
        """
        with self.assertRaises(exceptions.HttpRedirectMovedPermanentlyError):
            raising.raise_for_http_status(
                resp_code=301,
                resp_msg="Moved",
                call_url="http://x"
            )
        return

    def test_known_4xx_status_raises_specific(self) -> None:
        """
            Verifies a known 4xx status raises the mapped exception type.

            :returns: ``None``
        """
        with self.assertRaises(exceptions.HttpNotFoundError):
            raising.raise_for_http_status(
                resp_code=404,
                resp_msg="Not Found",
                call_url="http://x"
            )
        return

    def test_known_5xx_status_raises_specific(self) -> None:
        """
            Verifies a known 5xx status raises the mapped exception type.

            :returns: ``None``
        """
        with self.assertRaises(exceptions.HttpInternalServerError):
            raising.raise_for_http_status(
                resp_code=500,
                resp_msg="Internal Server Error",
                call_url="http://x"
            )
        return

    def test_unknown_3xx_status_raises_base(self) -> None:
        """
            Verifies an unknown 3xx status raises the 3xx base type.

            :returns: ``None``
        """
        captured = None
        try:
            raising.raise_for_http_status(
                resp_code=399,
                resp_msg="Strange",
                call_url="http://x"
            )
        except exceptions.HttpResponse3xxError as ex:
            captured = ex
        self.assertIsNotNone(captured)
        return

    def test_unknown_4xx_status_raises_base(self) -> None:
        """
            Verifies an unknown 4xx status raises the 4xx base type.

            :returns: ``None``
        """
        captured = None
        try:
            raising.raise_for_http_status(
                resp_code=499,
                resp_msg="Strange",
                call_url="http://x"
            )
        except exceptions.HttpResponse4xxError as ex:
            captured = ex
        self.assertIsNotNone(captured)
        return

    def test_unknown_5xx_status_raises_base(self) -> None:
        """
            Verifies an unknown 5xx status raises the 5xx base type.

            :returns: ``None``
        """
        captured = None
        try:
            raising.raise_for_http_status(
                resp_code=599,
                resp_msg="Strange",
                call_url="http://x"
            )
        except exceptions.HttpResponse5xxError as ex:
            captured = ex
        self.assertIsNotNone(captured)
        return

    def test_out_of_range_status_raises_http_exception(self) -> None:
        """
            Verifies a status code outside the documented ranges raises a
            :class:`HTTPException`.

            :returns: ``None``
        """
        captured = None
        try:
            raising.raise_for_http_status(
                resp_code=600,
                resp_msg="Out of range",
                call_url="http://x"
            )
        except HTTPException as ex:
            captured = ex
        self.assertIsNotNone(captured)
        return

    def test_raised_message_includes_url_and_context(self) -> None:
        """
            Verifies the raised exception message includes the URL and the
            supplied context.

            :returns: ``None``
        """
        captured = None
        try:
            raising.raise_for_http_status(
                resp_code=404,
                resp_msg="Not Found",
                call_url="http://example.com/missing",
                context="lookup failed"
            )
        except exceptions.HttpNotFoundError as ex:
            captured = ex
        self.assertIsNotNone(captured)
        msg = str(captured)
        self.assertIn("404", msg)
        self.assertIn("Not Found", msg)
        self.assertIn("http://example.com/missing", msg)
        self.assertIn("lookup failed", msg)
        return

    def test_raised_with_explicit_cause(self) -> None:
        """
            Verifies that the helper preserves an outer ``raise from`` chain
            when wrapped.

            :returns: ``None``
        """
        original = ValueError("root")
        captured = None
        try:
            try:
                raise original
            except ValueError as ve:
                try:
                    raising.raise_for_http_status(
                        resp_code=503,
                        resp_msg="Down",
                        call_url="http://x"
                    )
                except exceptions.HttpServiceUnavailableError as inner:
                    raise inner from ve
        except exceptions.HttpServiceUnavailableError as outer:
            captured = outer
        self.assertIsNotNone(captured)
        self.assertIs(captured.__cause__, original)
        return


class TestStatusToExceptionTable(unittest.TestCase):
    """
        Verifies that the documented status-to-exception mapping is consistent.
    """

    def test_table_only_contains_documented_codes(self) -> None:
        """
            Verifies every key in the table is an int in [300, 599].

            :returns: ``None``
        """
        for code in raising.STATUS_TO_EXCEPTION_TABLE.keys():
            is_int = isinstance(code, int)
            self.assertTrue(is_int)
            in_range = 300 <= code <= 599
            self.assertTrue(in_range, f"Code {code} out of expected range")
        return

    def test_table_values_are_http_exception_subclasses(self) -> None:
        """
            Verifies every mapped class is an :class:`HTTPException` subclass.

            :returns: ``None``
        """
        for code, klass in raising.STATUS_TO_EXCEPTION_TABLE.items():
            is_http = issubclass(klass, HTTPException)
            self.assertTrue(is_http, f"Code {code} maps to non-HTTPException")
        return


if __name__ == "__main__":
    unittest.main()
