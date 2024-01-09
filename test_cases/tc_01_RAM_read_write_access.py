from super_test_case import SuperTestCase
from Communications.ssh_connection import SshConnection
from Communications.communication_channels import SshCommunicationChannel
from logger import Logger


class TestCase(SuperTestCase):
    test_name = "TC_01"
    log_file_name = "TC_01_logs"

    def __init__(self, report):
        SuperTestCase.__init__(self, report)
        self.ssh = SshConnection(ssh_settings=SshCommunicationChannel())
        self.logger = Logger(self.test_name, self.log_file_name)
        self.total_memory = 0
        self.used_memory = 0
        self.free_memory = 0
        self.available_memory = 0
        self.disk_location = "/mnt/memtest1"
        self.memory_blocks_to_test = 100
        self.random_file_size_MB = 1
        self.random_file = "random_data"
        self.random_file_copy = "random_data_copy"
        self.file_list = []

    def setup(self):
        pass

    def main_test(self):
        self.get_ram_memory_size()
        self.make_dir_for_mounted_ramdisk()
        self.mount_disk()
        self.write_data_blocks_to_disk()
        self.md5sum_test()

    def teardown(self):
        self.remove_mounted_disk()
        self.delete_files()

    def get_ram_memory_size(self):
        free_mem = self.ssh.snd_cmd("free -m | sed -n \"2p\"")
        self.total_memory = int(free_mem.split()[1])
        self.used_memory = int(free_mem.split()[2])
        self.free_memory = int(free_mem.split()[3])
        self.available_memory = int(free_mem.split()[6])
        self.logger.info("LPDDR4 SDRAM size: ")
        self.logger.info("Total memory: {}".format(self.total_memory))
        self.logger.info("Used memory: {}".format(self.used_memory))
        self.logger.info("Free memory: {}".format(self.free_memory))
        self.logger.info("Available memory: {}".format(self.available_memory))

    def make_dir_for_mounted_ramdisk(self):
        command = "sudo mkdir -p {}".format(self.disk_location)
        self.ssh.snd_cmd(command)

    def mount_disk(self):
        command = "sudo mount -o size=3G -t tmpfs none {}".format(self.disk_location)
        self.ssh.snd_cmd(command)

    def write_data_blocks_to_disk(self):
        for mem_block in range(self.memory_blocks_to_test):
            outfile = "{}/{}_{:05d}".format(self.disk_location, self.random_file, mem_block)
            command = "dd if=/dev/urandom of={} bs=1M count={:d} 2>&1".\
                format(outfile, self.random_file_size_MB)
            result = self.ssh.snd_cmd(command)
            self.logger.info(result)
            self.file_list.append("{}_{:05d}".format(self.random_file, mem_block))

    def md5sum_test(self):
        self.logger.info("Calculating checksum for existing memory blocks: ")
        for i in range(len(self.file_list)):
            outfile = "{}/{}".format(self.disk_location, self.file_list[i])
            command = "md5sum {}".format(outfile)
            checksum = self.ssh.snd_cmd(command).split()[0]
            command = "cp {} {}_{:05d}".format(outfile, self.random_file_copy, i)
            self.ssh.snd_cmd(command)
            command = "md5sum {}_{:05d}".format(self.random_file_copy, i)
            checksum_copy = self.ssh.snd_cmd(command).split()[0]
            if checksum != checksum_copy:
                self.report_error("File copy has wrong checksum")

    def delete_files(self):
        self.logger.info("Deleting all memory blocks: ")
        command = "sudo rm {}/{}*".format(self.disk_location, self.random_file)
        result = self.ssh.snd_cmd(command)
        if "No such file or directory" in result:
            self.report_error("There is no such file or directory")

    def remove_mounted_disk(self):
        command = "sudo umount {} 2>&1".format(self.disk_location)
        result = self.ssh.snd_cmd(command)
        if "no mount point specified" in result:
            self.report_error("{} is not mounted. It does not exist.".format(self.disk_location))


if __name__ == "__main__":
    import test_runner

    test_runner.main()
