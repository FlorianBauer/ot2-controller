from typing import Optional
from uuid import UUID

from sila2.server import SilaServer

from .feature_implementations.ot2controller_impl import Ot2ControllerImpl
from .generated.ot2controller import Ot2ControllerFeature


class Server(SilaServer):
    def __init__(self, server_uuid: Optional[UUID] = None):
        # TODO: fill in your server information
        super().__init__(
            server_name="TODO",
            server_type="TODO",
            server_version="0.1",
            server_description="TODO",
            server_vendor_url="https://gitlab.com/SiLA2/sila_python",
            server_uuid=server_uuid,
        )

        self.ot2controller = Ot2ControllerImpl()

        self.set_feature_implementation(Ot2ControllerFeature, self.ot2controller)
