from multiprocessing import Process, Queue
from schemas import PostUserMessage


class DisplaySink(Process):
    def __init__(self, input: Queue[PostUserMessage]) -> None:
        super().__init__()
        self.input = input

    def run(self) -> None:
        while True:
            msg = self.input.get()
            user = msg.user_alias
            message = msg.message

