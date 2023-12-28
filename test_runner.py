import sys
import pathlib
import os
from importlib import import_module

from super_test_case import TestCaseReport


class TestRunner:

    def __init__(self):
        pass

    @staticmethod
    def _prepare_run():
        test_file = sys.argv[0]
        path_to_script = pathlib.PurePath(test_file)
        path1 = os.environ["PYTHONPATH"]
        sys_path = pathlib.PurePath(path1)
        module_path = path_to_script.relative_to(sys_path).as_posix().replace('/', '.').replace(".py", "")
        test_module = import_module(module_path)
        test_case_class = getattr(test_module, 'TestCase')
        report = TestCaseReport(test_case_class.log_file_name)
        return test_case_class, report

    def run_test(self):
        test_case, report = self._prepare_run()
        test_case(report).run()


def main():
    return TestRunner().run_test()
