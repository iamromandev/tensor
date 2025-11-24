from src.core.base import BaseSchema


class ImageInSchema(BaseSchema):
    prompt: str
    steps: int = 10
    width: int = 256
    height: int = 256

class ImageOutSchema(BaseSchema):
    output: str
