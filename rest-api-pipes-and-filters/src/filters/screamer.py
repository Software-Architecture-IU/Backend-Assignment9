from .base import BaseFilter
from schemas import PostUserMessage


class Screamer(BaseFilter):
    def process(self, msg: PostUserMessage):
        print("Screamer resieved:", msg.message)
        res = PostUserMessage(message=msg.message.upper(), user_alias=msg.user_alias)
        return res
