import subprocess


class SSHClient:
    def __init__(self, hostname, key_path):
        self.hostname = hostname
        self.key_path = key_path

    def run(self, command):
        result = subprocess.run(
            [
                "ssh",
                "-i", self.key_path,
                "-o", "BatchMode=yes",
                "-o", "StrictHostKeyChecking=no",
                self.hostname,
                command
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
