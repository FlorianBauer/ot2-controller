from __future__ import annotations

from typing import Any, Dict, List

from sila2.framework import FullyQualifiedIdentifier

from ..generated.ot2controller import Ot2ControllerBase, CameraPicture_Response


class Ot2ControllerImpl(Ot2ControllerBase):
    def get_Connection(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> str:
        raise NotImplementedError  # TODO

    def get_AvailableProtocols(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> List[str]:
        raise NotImplementedError  # TODO

    def get_CameraPicture(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> CameraPicture_Response:
        raise NotImplementedError  # TODO

    def UploadProtocol(
        self, ProtocolSourcePath: str, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> None:
        raise NotImplementedError  # TODO

    def RemoveProtocol(
        self, ProtocolFile: str, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> None:
        raise NotImplementedError  # TODO

    def RunProtocol(
        self, ProtocolFile: str, IsSimulating: bool, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> int:
        raise NotImplementedError  # TODO
