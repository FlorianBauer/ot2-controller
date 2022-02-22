from __future__ import annotations

from typing import NamedTuple


class UploadProtocol_Responses(NamedTuple):

    pass


class RemoveProtocol_Responses(NamedTuple):

    pass


class RunProtocol_Responses(NamedTuple):

    ReturnValue: int
    """
    The returned value from the executed protocol. On a simulated execution, only the value 0
                is indicating a successful simulation.
            
    """
