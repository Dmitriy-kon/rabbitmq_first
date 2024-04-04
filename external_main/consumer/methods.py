import json

from aiormq.abc import DeliveredMessage
from starlette.websockets import WebSocketDisconnect

from chat.views import manager
from color_formatter import color_f

async def chat_massage_from_internal(message: DeliveredMessage):
    
    incom_message = json.loads(message.body.decode())
    print(f"{color_f.red}[ x ] Message: {incom_message} was received from consumer. This is exernal main{color_f.default}")
    
    username = incom_message["username"]
    socket = manager.users.get(username)
    
    try:
        # await manager.send_json(incom_message, socket)
        await manager.broadcast_json(incom_message)
    except WebSocketDisconnect:
        manager.disconnect(socket, username)

    await message.channel.basic_ack(message.delivery.delivery_tag)

    