from typing import Optional
from uuid import UUID

from sila2.server import SilaServer

from . import __version__
from .feature_implementations.ot2controller_impl import Ot2ControllerImpl
from .generated.ot2controller import Ot2ControllerFeature


class Server(SilaServer):
    def __init__(self, server_uuid: Optional[UUID] = None):
        super().__init__(
            server_name="Ot2Controller",
            server_type="OpentronsOt2Controller",
            server_version=__version__,
            server_description=(
                "A SiLA 2 service enabling the execution of python protocols on a Opentrons 2 liquid handler."
            ),
            server_vendor_url="https://github.com/FlorianBauer/ot2-controller",
            server_uuid=server_uuid,
        )

        self.ot2controller = Ot2ControllerImpl()

        self.set_feature_implementation(Ot2ControllerFeature, self.ot2controller)
