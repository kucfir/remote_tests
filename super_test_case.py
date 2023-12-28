import abc

from logger import Logger


class TestAbortedException(Exception):
    pass


class TestCaseReport:

    def __init__(self, log_file_name):
        self._error_count = 0
        self.log_file_name = log_file_name

    def report_error(self, message):
        self._error_count += 1
        Logger("ERROR REPORTED: ", self.log_file_name).error(message)

    def test_aborted(self, message):
        raise TestAbortedException(message)


class SuperTestCase(abc.ABC):
    description = None

    def __init__(self, report):
        self.__report = report

    def report_error(self, message=""):
        self.__report.report_error(message)

    def abort_test(self, message=""):
        self.__report.test_aborted(message)

    def run(self):
        self.setup()
        self.main_test()

    @abc.abstractmethod
    def setup(self):
        raise Exception("Overwrite this abstract method in your TC!")

    @abc.abstractmethod
    def main_test(self):
        raise Exception("Overwrite this abstract method in your TC!")

    @abc.abstractmethod
    def teardown(self):
        raise Exception("Overwrite this abstract method in your TC!")
