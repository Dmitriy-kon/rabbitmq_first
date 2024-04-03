
import json
from aiormq.abc import DeliveredMessage

from .color_formatter import color_f

async def simple_message(message: DeliveredMessage):
    print(f"{color_f.red}Message: {message.body}{color_f.default}")
    
async def simple_message_ack(message: DeliveredMessage):
    print(f"{color_f.red}Message with ack: {message.body}{color_f.default}")
    await message.channel.basic_ack(message.delivery.delivery_tag)


async def json_message(message: DeliveredMessage):
    pass
    # json_message = json.loads(message.body.decode())
    # # json_message = message.body.decode
    # print(json_message.get("message"))
    # print(json_message.get("type"))
    
    # print(f"{color_f.red}Message: {json_message}{color_f.default}")
    # await message.channel.basic_ack(message.delivery.delivery_tag)