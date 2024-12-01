from base import BaseFilter
from schemas import PostUserMessage


class Screamer(BaseFilter):
    def process(self, msg: PostUserMessage):
        res = PostUserMessage()
        res.message = msg.message.upper()
        res.user_alias = msg.user_alias
        return res
