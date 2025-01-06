from pydantic import BaseModel, HttpUrl


class FileData(BaseModel):
    key: str
    src: HttpUrl | str
    size: int
    filename: str
    content_type: str
