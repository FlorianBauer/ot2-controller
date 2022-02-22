from __future__ import annotations

from typing import Optional

from sila2.framework.errors.defined_execution_error import DefinedExecutionError

from .ot2controller_feature import Ot2ControllerFeature


class UploadFileFailed(DefinedExecutionError):
    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "The upload of the file to the OT-2 device failed."
        super().__init__(Ot2ControllerFeature.defined_execution_errors["UploadFileFailed"], message=message)


class RemoveFileFailed(DefinedExecutionError):
    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "The file on the OT-2 device does not exist or could not be removed."
        super().__init__(Ot2ControllerFeature.defined_execution_errors["RemoveFileFailed"], message=message)
