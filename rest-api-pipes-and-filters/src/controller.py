from fastapi import APIRouter, HTTPException

from rabbitmq import rabbitmq_producer
from schemas import PostUserMessage

router = APIRouter(prefix="")

producer = rabbitmq_producer


@router.post("/message")
async def post_message(body: PostUserMessage) -> None:
    username = body.user_alias
    msg = body.message

    if is_empty(username):
        raise HTTPException(404, f'User {username} not found')

    if is_empty(msg):
        raise HTTPException(404, f'Message {msg} not found')

    producer.publish_message(body.json())


def is_empty(string: str) -> bool:
    return string == '' or string is None
