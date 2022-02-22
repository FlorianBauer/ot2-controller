from __future__ import annotations

from typing import Any, Dict, List

from sila2.framework import FullyQualifiedIdentifier

from ..generated.ot2controller import (
    Ot2ControllerBase,
    RemoveProtocol_Responses,
    RunProtocol_Responses,
    UploadProtocol_Responses,
)


class Ot2ControllerImpl(Ot2ControllerBase):
    def get_Connection(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> str:
        raise NotImplementedError  # TODO

    def get_AvailableProtocols(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> List[str]:
        raise NotImplementedError  # TODO

    def get_CameraPicture(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Any:
        raise NotImplementedError  # TODO

    def UploadProtocol(
        self, ProtocolSourcePath: str, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> UploadProtocol_Responses:
        raise NotImplementedError  # TODO

    def RemoveProtocol(
        self, ProtocolFile: str, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> RemoveProtocol_Responses:
        raise NotImplementedError  # TODO

    def RunProtocol(
        self, ProtocolFile: str, IsSimulating: bool, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> RunProtocol_Responses:
        raise NotImplementedError  # TODO
