from __future__ import annotations

from datetime import datetime
from typing import NamedTuple


class CameraPicture_Response(NamedTuple):
    ImageData: bytes
    """The *.jpg image"""
    ImageTimestamp: datetime
    """The timestamp when the image was taken"""

class CameraMovie_Response(NamedTuple):
    VideoData: bytes
    """The *.mp4 video"""
    VideoTimestamp: datetime
    """The timestamp when the video was taken"""