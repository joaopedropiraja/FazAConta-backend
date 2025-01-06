from fazaconta_backend.modules.user.domain.Device import Device
from fazaconta_backend.modules.user.domain.Pix import Pix
from fazaconta_backend.modules.user.domain.UserEmail import UserEmail
from fazaconta_backend.modules.user.domain.UserPassword import UserPassword
from fazaconta_backend.modules.user.domain.UserPhoneNumber import UserPhoneNumber
from fazaconta_backend.modules.user.events.UserCreated import UserCreated
from fazaconta_backend.shared.domain.Entity import Entity
from fazaconta_backend.shared.domain.Guard import Guard
from fazaconta_backend.shared.domain.UniqueEntityId import UniqueEntityId
from fazaconta_backend.shared.domain.files.FileData import FileData


class User(Entity):
    user_name: str
    email: UserEmail
    password: UserPassword
    image_src: str | None
    pix: str | None

    def __init__(
        self,
        email: UserEmail,
        user_name: str,
        password: UserPassword,
        image_src: str | None = None,
        pix: str | None = None,
        id: UniqueEntityId | None = None,
    ):
        super().__init__(id)

        Guard.against_undefined(argument=user_name, argument_name="user_name")

        self.email = email
        self.password = password
        self.user_name = user_name
        self.image_src = image_src
        self.pix = pix

        is_new_user = id is None
        if is_new_user:
            self.add_domain_event(UserCreated(self.id))


# # The User class
# class User(Entity):

#     def __init__(
#         self,
#         name: str,
#         nickname: str,
#         email: UserEmail,
#         password: UserPassword,
#         phone_number: UserPhoneNumber,
#         profile_photo: FileData | None = None,
#         pic: Pix | None = None,
#         devices: list[Device] | None = None,
#         id: UniqueEntityId | None = None,
#     ) -> None:

#         Guard.against_undefined_bulk(
#             [
#                 {"argument": name, "argumentName": "name"},
#                 {"argument": nickname, "argumentName": "nickname"},
#             ]
#         )

#         super().__init__(id)

#         self._name = name
#         self._nickname = nickname
#         self._email = email
#         self._password = password
#         self._phone_number = phone_number
#         self._profile_photo = profile_photo
#         self._pic = pic
#         self._devices = devices or []

#         is_new_user = id is None
#         if is_new_user:
#             self.add_domain_event(UserCreated(self.id))

#     @property
#     def name(self) -> str:
#         return self._name

#     @property
#     def nickname(self) -> str:
#         return self._nickname

#     @property
#     def email(self) -> UserEmail:
#         return self._email

#     @property
#     def password(self) -> UserPassword:
#         return self._password

#     @property
#     def phone_number(self) -> UserPhoneNumber:
#         return self._phone_number

#     @property
#     def profile_photo(self) -> FileData | None:
#         return self._profile_photo

#     @property
#     def pic(self) -> Pix | None:
#         return self._pic

#     @property
#     def devices(self) -> list[Device]:
#         return self._devices

#     @name.setter
#     def name(self, value: str) -> None:
#         self._name = value

#     @nickname.setter
#     def nickname(self, value: str) -> None:
#         self._nickname = value

#     @password.setter
#     def password(self, value: UserPassword) -> None:
#         self._password = value

#     @phone_number.setter
#     def phone_number(self, value: UserPhoneNumber) -> None:
#         self._phone_number = value

#     @profile_photo.setter
#     def profile_photo(self, value: FileData | None) -> None:
#         self._profile_photo = value

#     @pic.setter
#     def pic(self, value: Pix | None) -> None:
#         self._pic = value

#     def add_device(self, device: Device) -> None:
#         self._devices.append(device)
