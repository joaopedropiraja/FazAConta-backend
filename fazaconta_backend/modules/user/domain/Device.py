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


# class Device(Entity):

#     def __init__(
#         self,
#         device_name: str,
#         platform: Platform,
#         push_token: str | None = None,
#         last_login_at: datetime | None = None,
#         id: UniqueEntityId | None = None,
#     ):
#         Guard.against_undefined_bulk(
#             [
#                 {"argument": device_name, "argumentName": "device_name"},
#                 {"argument": platform, "argumentName": "platform"},
#             ]
#         )
#         Guard.is_one_of_enum(
#             value=platform, enum_class=Platform, argument_name="Plataform"
#         )

#         super().__init__(id)

#         self._device_name = device_name
#         self._platform = platform
#         self._push_token = push_token
#         self._last_login_at = last_login_at

#     @property
#     def device_name(self) -> str:
#         return self._device_name

#     @property
#     def platform(self) -> Platform:
#         return self._platform

#     @property
#     def push_token(self) -> str | None:
#         return self._push_token

#     @property
#     def last_login_at(self) -> datetime | None:
#         return self._last_login_at

#     @push_token.setter
#     def push_token(self, value: str) -> None:
#         self._push_token = value

#     @last_login_at.setter
#     def last_login_at(self, value: datetime) -> None:
#         self._last_login_at = value
