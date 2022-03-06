from __future__ import annotations

from datetime import datetime
from typing import NamedTuple


class CameraPicture_Response(NamedTuple):
    ImageData: bytes
    """The *.jpg image"""
    ImageTimestamp: datetime
    """The timestamp when the image was taken"""
