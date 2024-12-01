from base import BaseFilter
from schemas import PostUserMessage


class Filter(BaseFilter):
    def process(self, msg: PostUserMessage):
        if not any(map(lambda x: x in {'ailurophobia', 'mango', 'bird-watching'},
                   msg.message.split())):
            return msg
        return None
