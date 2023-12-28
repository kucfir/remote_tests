import socket

import paramiko

from Communications.communication_channels import SshCommunicationChannel


class SshConnection:

    def __init__(self, ssh_settings: SshCommunicationChannel):
        self.ip = ssh_settings.ip
        self.port = ssh_settings.port
        self.username = ssh_settings.username
        self.password = ssh_settings.password
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5.0)
        self.socket.connect((self.ip, self.port))
        self.transport = paramiko.Transport(self.socket)
        self.transport.connect(username=self.username, password=self.password)
        self.shell = self.transport.open_session()
        self.receive_buffer = bytearray()

    @staticmethod
    def create_ssh_channel():
        return SshConnection(SshCommunicationChannel())

    def connect(self):
        self.socket.connect((self.ip, self.port))

    def close(self):
        self.transport.close()
        self.socket.close()

    def snd_cmd(self, command):
        ssh = self.create_ssh_channel()
        ssh.shell.exec_command(command)
        self.receive_buffer = ssh.shell.recv(10 * 1024)
        return self.receive_buffer.decode("ascii", errors="ignore")
