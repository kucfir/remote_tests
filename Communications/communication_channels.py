class SshCommunicationChannel:
    """SSH connection parameters."""

    def __init__(self, ip: str = "", port: int = 22, username: str = "", password: str = ""):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password

    def __str__(self):
        return "{}:{}".format(self.ip, self.port)
