from fastapi import APIRouter, HTTPException
from schemas import PostUserMessage
from main import g_Processes

router = APIRouter(prefix="")


@router.post("/message")
async def post_message(body: PostUserMessage) -> None:
    username = body.user_alias
    msg = body.message

    if is_empty(username):
        raise HTTPException(404, f'User {username} not found')

    if is_empty(msg):
        raise HTTPException(404, f'Message {msg} not found')

    g_Processes[0].input.put(body)


def is_empty(string: str) -> bool:
    return string == '' or string is None
