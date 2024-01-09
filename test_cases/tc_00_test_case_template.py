from super_test_case import SuperTestCase
from Communications.ssh_connection import SshConnection
from Communications.communication_channels import SshCommunicationChannel
from logger import Logger


class TestCase(SuperTestCase):
    test_name = "TC_00"
    log_file_name = "TC_00_logs"

    def __init__(self, report):
        SuperTestCase.__init__(self, report)
        self.ssh = SshConnection(ssh_settings=SshCommunicationChannel())
        self.logger = Logger(self.test_name, self.log_file_name)

    def setup(self):
        pass

    def main_test(self):
        pass

    def teardown(self):
        pass


if __name__ == "__main__":
    import test_runner

    test_runner.main()