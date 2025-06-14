"""
    .. module:: itestjob
        :platform: Darwin, Linux, Unix, Windows
        :synopsis: Module that contains the `ITestJob` protocol object which provides common patterns
                   for working for a variety of test jobs.

    .. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Protocol, List

class ITestJob(Protocol):
    """
        The :class:`ITestJob` interface defines a common protocol for
        implementing test jobs.
    """

    @property
    def importerrors(self):
        """
            A list of import errors that occurred when the job was loaded.

            :returns: A list of exceptions raised during job import.
        """
    
    def begin(self) -> None:
        """
            Called at the beginning of a test job in order to setup the recording of test results.

            :returns: ``None``
        """

    def execute(self) -> int:
        """
            Executes the test job.

            :returns: An integer where ``0`` indicates success.
        """

    def finalize(self) -> None:
        """
            Called at the end of a test job in order to flush the results of the test run and
            copy the report template to the output directory.

            :returns: ``None``
        """

    def query(self, query: str, format: int=0) -> List[Any]:
        """
            Queries the test job for information about the tests it will run and the resource
            requirements of those tests.

            :param query: The query string to execute against the job.
            :param format: Optional format identifier for the query results.

            :returns: A list of query results.
        """
