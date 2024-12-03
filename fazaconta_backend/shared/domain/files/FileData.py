from pydantic import BaseModel, HttpUrl


class FileData(BaseModel):
    url: HttpUrl | str = ""
    size: int = 0
    filename: str = ""
    content_type: str = ""
