from src.core.base import BaseSchema


class RunSchema(BaseSchema):
    prompt: str

class RunOutSchema(BaseSchema):
    output: str
