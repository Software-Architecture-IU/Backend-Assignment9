from fastapi import APIRouter, HTTPException

from rabbitmq import rabbitmq_producer, rabbitmq_consumer
from schemas import PostUserMessage, PostMessageReply
from datetime import datetime

import os


router = APIRouter(prefix="")

producer = rabbitmq_producer
consumer = rabbitmq_consumer


@router.post("/message", response_model=PostMessageReply)
async def post_message(body: PostUserMessage) -> None:
    username = body.user_alias
    msg = body.message
    request_start_timestamp = datetime.now().timestamp()

    if is_empty(username):
        raise HTTPException(404, f'User {username} not found')

    if is_empty(msg):
        raise HTTPException(404, f'Message {msg} not found')

    producer.publish_message(body.json())
    mes = consumer.consume_one_message()

    if os.getenv("PERFORMANCE_TEST") == "true":
        while mes is None:
            mes = consumer.consume_one_message()

    ack_timestamp = datetime.now().timestamp()
    return PostMessageReply(
        timestamp=str(ack_timestamp - request_start_timestamp))


def is_empty(string: str) -> bool:
    return string == '' or string is None
