from __future__ import annotations

from typing import TYPE_CHECKING

from sila2.client import SilaClient

from .ot2controller import Ot2ControllerFeature, RemoveFileFailed, UploadFileFailed

if TYPE_CHECKING:

    from .ot2controller import Ot2ControllerClient


class Client(SilaClient):

    Ot2Controller: Ot2ControllerClient

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._register_defined_execution_error_class(
            Ot2ControllerFeature.defined_execution_errors["UploadFileFailed"], UploadFileFailed
        )

        self._register_defined_execution_error_class(
            Ot2ControllerFeature.defined_execution_errors["RemoveFileFailed"], RemoveFileFailed
        )
