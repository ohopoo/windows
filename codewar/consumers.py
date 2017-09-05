import json
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from .tasks import start_compile


@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({
        "text": json.dumps({
            "state": "ready !",
            'message':""
        })
    })

@channel_session_user
def ws_receive(message):
    try:
        data = json.loads(message['text'])
    except ValueError:
        return

    if data:
        reply_channel = message.reply_channel.name
        if data['action'] == "compile_run":
            start_compile(message.user.username, data['data'], reply_channel)
