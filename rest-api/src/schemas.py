from pydantic import BaseModel


class PostUserMessage(BaseModel):
    user_alias: str
    message: str
