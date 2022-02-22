from __future__ import annotations

from typing import Any, Iterable, List, Optional

from ot2controller_types import RemoveProtocol_Responses, RunProtocol_Responses, UploadProtocol_Responses
from sila2.client import ClientMetadataInstance, ClientUnobservableProperty

class Ot2ControllerClient:
    """
    A SiLA 2 complaint controller for an OT-2 liquid handler.
    """

    Connection: ClientUnobservableProperty[str]
    """
    Connection details of the remote OT-2.
    """

    AvailableProtocols: ClientUnobservableProperty[List[str]]
    """
    List of the stored files available on the OT-2.
    """

    CameraPicture: ClientUnobservableProperty[Any]
    """
    A current picture from the inside of the OT-2 made with the built-in camera.
    """

    def UploadProtocol(
        self, ProtocolSourcePath: str, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> UploadProtocol_Responses:
        """
        Uploads the given Protocol to the "/data/user_storage" directory on the OT-2.
        """
        ...
    def RemoveProtocol(
        self, ProtocolFile: str, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> RemoveProtocol_Responses:
        """
        Removes the given Protocol from the "/data/user_storage" directory on the OT-2.
        """
        ...
    def RunProtocol(
        self, ProtocolFile: str, IsSimulating: bool, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> RunProtocol_Responses:
        """
        Runs the given Protocol on the OT-2.
        """
        ...
