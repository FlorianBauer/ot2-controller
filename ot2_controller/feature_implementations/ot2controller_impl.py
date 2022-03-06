from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import paramiko
from paramiko.client import SSHClient
from paramiko.pkey import PKey
from scp import SCPClient, SCPException
from sila2.framework import FullyQualifiedIdentifier

from ..generated.ot2controller import CameraPicture_Response, Ot2ControllerBase

DEFAULT_SSH_PRIVATE_KEY: str = "~/.ssh/ot2_ssh_key"
DEVICE_USERNAME: str = "root"
USER_STORAGE_DIR: str = "/data/user_storage/"


class Ot2ControllerImpl(Ot2ControllerBase):
    device_ip: str
    """Path to the SSH private key file"""
    pkey: PKey
    """The actual private key used by Paramiko"""
    ssh: SSHClient
    """The SSH client used by Paramiko"""

    def __init__(self, device_ip: str, pkey_path: Optional[str] = None):
        self.device_ip = device_ip
        # The the location of the generated private key.
        # https://support.opentrons.com/en/articles/3203681-setting-up-ssh-access-to-your-ot-2
        # https://hackersandslackers.com/automate-ssh-scp-python-paramiko/
        if pkey_path is None:
            self.pkey = paramiko.RSAKey.from_private_key_file(str(Path(DEFAULT_SSH_PRIVATE_KEY).expanduser().resolve()))
        else:
            self.pkey = paramiko.RSAKey.from_private_key_file(str(Path(pkey_path).expanduser().resolve()))

        self.ssh = paramiko.SSHClient()
        # Load SSH host keys.
        self.ssh.load_system_host_keys()
        # Add SSH host key automatically if needed.
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connect to device using key file authentication.
        self.ssh.connect(hostname=device_ip, username=DEVICE_USERNAME, pkey=self.pkey, look_for_keys=False)

        self.__logger = logging.getLogger(self.__class__.__name__)

    def get_Connection(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> str:
        return f"Device IP: {self.device_ip}, SSH key fingerprint: {self.pkey.get_fingerprint().hex()}"

    def get_AvailableProtocols(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> List[str]:
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(f"ls {USER_STORAGE_DIR}")
        return [line.strip() for line in ssh_stdout.readlines() if line.endswith(".py")]

    def get_CameraPicture(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> CameraPicture_Response:
        out_image_file: str = "/tmp/tmp_image.jpeg"
        cmd: str = f"ffmpeg -y -f video4linux2 -s 640x480 -i /dev/video0 -ss 0:0:1 -frames 1 {out_image_file}"

        self.__logger.debug(f"run '{cmd}'")
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
        run_ret: int = ssh_stdout.channel.recv_exit_status()
        self.__logger.debug(f"run returned '{str(run_ret)}'")

        scp = SCPClient(self.ssh.get_transport())
        try:
            scp.get(out_image_file, "/tmp/tmp_image.jpeg", recursive=False)
            self.__logger.debug(f"Downloaded {out_image_file} to /tmp/tmp_image.jpeg")
        except SCPException as error:
            self.__logger.error(error)
            raise
        finally:
            scp.close()

        return CameraPicture_Response(
            ImageData=open("/tmp/tmp_image.jpeg", "rb").read(), ImageTimestamp=datetime.now(timezone.utc)
        )

    def UploadProtocol(self, ProtocolSourcePath: str, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        scp = SCPClient(self.ssh.get_transport())
        file: str = str(Path(ProtocolSourcePath).expanduser().resolve())

        try:
            scp.put(file, recursive=True, remote_path=USER_STORAGE_DIR)
        except SCPException as error:
            self.__logger.error(error)
            raise
        finally:
            scp.close()

        self.__logger.debug(f"Uploaded {file} to {USER_STORAGE_DIR}")

    def RemoveProtocol(self, ProtocolFile: str, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        protocol: str = ProtocolFile.strip()
        if not protocol.endswith(".py"):
            raise ValueError("The file is not a python protocol.")

        file: str = str(Path(USER_STORAGE_DIR + protocol))
        self.__logger.debug(f"remove: {file}")

        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(f"rm {file}")
        # TODO: remove debug logs on release
        self.__logger.debug(ssh_stdout.readlines())
        self.__logger.debug(ssh_stderr.readlines())
        remove_ret: int = ssh_stdout.channel.recv_exit_status()
        self.__logger.debug(f"remove returned '{str(remove_ret)}'")
        if remove_ret != 0:
            raise ValueError(f"The removal of the file '{file}' was not successful.")

    def RunProtocol(
        self, ProtocolFile: str, IsSimulating: bool, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> int:
        if IsSimulating:
            cmd: str = f"python3 -m opentrons.simulate {USER_STORAGE_DIR}{ProtocolFile}"
        else:
            cmd: str = f"python3 -m opentrons.execute {USER_STORAGE_DIR}{ProtocolFile}"

        self.__logger.debug(f"run '{cmd}'")
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)

        for line in ssh_stderr.readlines():
            print(line, end="")

        for line in ssh_stdout.readlines():
            print(line, end="")

        run_ret: int = ssh_stdout.channel.recv_exit_status()
        self.__logger.debug("run returned '" + str(run_ret) + "'")

        if IsSimulating and run_ret != 0:
            raise ValueError("The simulation of the protocol was not successful.")

        return run_ret

    def __del__(self):
        # Close connection
        self.ssh.close()
