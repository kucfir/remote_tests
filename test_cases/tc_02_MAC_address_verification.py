import re

from super_test_case import SuperTestCase
from Communications.ssh_connection import SshConnection
from Communications.communication_channels import SshCommunicationChannel
from logger import Logger


class TestCase(SuperTestCase):
    test_name = "TC_02"
    log_file_name = "TC_02_logs"

    def __init__(self, report):
        SuperTestCase.__init__(self, report)
        self.ssh = SshConnection(ssh_settings=SshCommunicationChannel())
        self.logger = Logger(self.test_name, self.log_file_name)

    def setup(self):
        pass

    def main_test(self):
        self.logger.info("MAC address: {}".format(self.read_wlan0_mac_address()))
        self.verify_wlan0_mac_address()

    def teardown(self):
        pass

    def read_wlan0_mac_address(self):
        return self.ssh.snd_cmd("cat /sys/class/net/wlan0/address")

    @staticmethod
    def check_mac_address_format(mac_address):
        if re.findall(r"([a-f0-9]{2}[:]){5}[a-f0-9]{2}", mac_address):
            result = True
        else:
            result = False
        return result

    def verify_wlan0_mac_address(self):
        mac_address = self.read_wlan0_mac_address()
        if self.check_mac_address_format(mac_address):
            self.logger.info("MAC address for wlan0: {} is correctly formatted.".format(mac_address))
        else:
            self.report_error("MAC address for wlan0: {} is wrong formatted.".format(mac_address))


if __name__ == "__main__":
    import test_runner

    test_runner.main()