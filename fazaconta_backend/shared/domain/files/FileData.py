from pydantic import HttpUrl

from fazaconta_backend.shared.domain.ValueObject import ValueObject


class FileData(ValueObject):
    key: str
    src: HttpUrl | str
    size: int
    filename: str
    content_type: str
