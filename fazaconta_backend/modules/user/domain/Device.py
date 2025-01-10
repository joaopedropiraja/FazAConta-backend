from datetime import datetime
from enum import Enum

from fazaconta_backend.shared.domain.ValueObject import ValueObject


class Platform(str, Enum):
    IOS = "ios"
    ANDROID = "android"


class Device(ValueObject):
    device_id: str
    device_name: str
    platform: Platform
    push_token: str | None
    last_login_at: datetime | None
