"""
.. module:: itestjob
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module that contains the `ITestJob` protocol object which is provides common patterns
               for working for a variety of test jobs.  

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>
"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2025, Automation Mojo LLC"
__credits__ = []


from typing import Any, Protocol, List

class ITestJob(Protocol):
    """
        The :class:`ISystemContext` interface is used to provide a common interface for both SSH and Serial command runners.
    """

    @property
    def importerrors(self):
        """
            A list of import errors that occurred when the job was loaded.
        """
    
    def begin(self) -> None:
        """
            Called at the beginning of a test job in order to setup the recording of test results.
        """

    def execute(self) -> int:
        """
            Executes the test job and returns an integer indicating if the test job was successful.  A return
            value of 0 indicates success.
        """

    def finalize(self) -> None:
        """
            Called at the end of a test job in order to flush the results of the test run, copy
            the report template to the output directory.
        """

    def query(self, query: str, format: int=0) -> List[Any]:
        """
            Queries the test job for information about the tests it will run and the resource requirements of those tests.
        """
