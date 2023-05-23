from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase

from .ot2controller_types import CameraPicture_Response, CameraMovie_Response


class Ot2ControllerBase(FeatureImplementationBase, ABC):

    """
    A SiLA 2 complaint controller for an OT-2 liquid handler.
    """

    @abstractmethod
    def get_Connection(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> str:
        """
        Connection details of the remote OT-2.

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Connection details of the remote OT-2.
        """
        pass

    @abstractmethod
    def get_AvailableProtocols(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> List[str]:
        """
        List of the stored files available on the OT-2.

        :param metadata: The SiLA Client Metadata attached to the call
        :return: List of the stored files available on the OT-2.
        """
        pass

    @abstractmethod
    def get_CameraPicture(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> CameraPicture_Response:
        """
        A current picture from the inside of the OT-2 made with the built-in camera.

        :param metadata: The SiLA Client Metadata attached to the call
        :return: A current picture from the inside of the OT-2 made with the built-in camera.
        """
        pass

    @abstractmethod
    def UploadProtocol(self, ProtocolSourcePath: str, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        Uploads the given Protocol to the "/data/user_storage" directory on the OT-2.

        :param ProtocolSourcePath: The path to the Protocol to upload.
        :param metadata: The SiLA Client Metadata attached to the call
        """
        pass

    @abstractmethod
    def RemoveProtocol(self, ProtocolFile: str, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> None:
        """
        Removes the given Protocol from the "/data/user_storage" directory on the OT-2.

        :param ProtocolFile: The file name of the Protocol to remove.
        :param metadata: The SiLA Client Metadata attached to the call
        """
        pass

    @abstractmethod
    def RunProtocol(
        self, ProtocolFile: str, IsSimulating: bool, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> int:
        """
        Runs the given Protocol on the OT-2.

        :param ProtocolFile: The file name of the Protocol to run.
        :param IsSimulating: Defines whether the protocol gets just simulated or actually executed on the device.
        :param metadata: The SiLA Client Metadata attached to the call
        :return:

            - ReturnValue: The returned value from the executed protocol. On a simulated execution, only the value 0
                is indicating a successful simulation.
        """
        pass

    @abstractmethod
    def CameraMovie(self, LengthOfVideo: str, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> CameraMovie_Response:
        """
        A current video from the inside of the OT-2 made with the built-in camera.

        :param lengthOfVideo: length of the video
        :param metadata: The SiLA Client Metadata attached to the call
        :return: A current movie from the inside of the OT-2 made with the built-in camera.
        """
        pass
