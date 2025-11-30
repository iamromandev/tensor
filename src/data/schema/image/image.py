from src.core.base import BaseSchema


class ImageInSchema(BaseSchema):
    prompt: str
    steps: int = 30
    width: int = 512
    height: int = 512

class ImageOutSchema(BaseSchema):
    output: str
